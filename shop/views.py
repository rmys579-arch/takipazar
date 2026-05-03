import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as auth_logout
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from cart.cart import Cart
from .models import Category, Product, Profile, Order
from .forms import OrderCreateForm
from .utils import start_3ds_payment  # Fonksiyon ismini doğrulayın

# ÜRÜN LİSTELEME VE ARAMA
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all() 
    products = Product.objects.filter(stock__gt=0)

    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories, 
        'products': products,
        'query': query
    })

# ÜRÜN DETAY
def product_detail(request, id, slug=None):
    if slug:
        product = get_object_or_404(Product, id=id, slug=slug)
    else:
        product = get_object_or_404(Product, id=id)
    categories = Category.objects.all()
    return render(request, 'shop/product/detail.html', {
      'product': product,
      'categories': categories
    })

# KAYIT OLMA
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect('shop:login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# ÇIKIŞ YAPMA
def custom_logout(request):
    auth_logout(request)
    return redirect('shop:product_list')

# PROFİL
@login_required
def profile(request):
    orders = Order.objects.filter(email=request.user.email).order_by('-created')
    return render(request, 'shop/profile.html', {
        'orders': orders,
        'user': request.user
    })

# SİPARİŞ OLUŞTURMA (3DS ENTEGRASYONLU)
@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        payment_method = request.POST.get('payment_method')

        if form.is_valid():
            # 1. Sipariş nesnesini oluştur ve kaydet
            order = form.save(commit=False)
            order.country_code = request.POST.get('country_code')
            order.payment_method = payment_method
            order.total_paid = cart.get_total_price()
            order.save() 

            if payment_method == 'kart':
                # 2. Kart bilgilerini al
                card_details = {
                    'card_name': request.POST.get('card_name'),
                    'card_number': request.POST.get('card_number').replace(" ", ""),
                    'expire_month': request.POST.get('expire_month'),
                    'expire_year': request.POST.get('expire_year'),
                    'cvc': request.POST.get('cvc'),
                }
                
                # 3. 3DS ödemeyi başlat
                result_json = start_3ds_payment(order, card_details, cart)
                
                # --- ENTEGRE EDİLEN GÜVENLİ JSON İŞLEME MANTIĞI ---
                if result_json:
                    try:
                        result = json.loads(result_json)
                    except (TypeError, json.JSONDecodeError):
                        # Eğer gelen veri zaten bir sözlükse veya json değilse
                        result = result_json if isinstance(result_json, dict) else {}
                else:
                    result = {}
                # ------------------------------------------------

                if result.get('status') == 'success':
                    # Banka SMS onay sayfasına (iyzico üzerinden) yönlendir
                    return HttpResponse(result.get('threeDSHtmlContent'))
                else:
                    # Hata durumunda mesajı göster ve geçici siparişi sil
                    error = result.get('errorMessage', 'Ödeme sistemi şu an yanıt vermiyor.')
                    order.delete()
                    return render(request, 'shop/checkout.html', {
                        'form': form, 
                        'cart': cart, 
                        'error_message': error
                    })
            else:
                # 4. Kapıda ödeme işlemleri
                _finalize_order(order, cart)
                return redirect('shop:order_success')
        else:
            # Form geçersizse hataları terminale bas
            print(f"FORM HATALARI: {form.errors}")
    else:
        form = OrderCreateForm()
    
    return render(request, 'shop/checkout.html', {'cart': cart, 'form': form})
@csrf_exempt
def payment_callback(request):
    status = request.POST.get('status')
    conversation_id = request.POST.get('conversationId')
    
    if status == 'success':
        order = get_object_or_404(Order, id=conversation_id)
        # Not: Callback anında sepeti temizlemek için ek mantık gerekebilir
        return render(request, 'cart/order_success.html', {'order_no': order.id})
    else:
        return render(request, 'shop/checkout.html', {
            'error_message': "3D Onayı alınamadı veya ödeme reddedildi."
        })

def _finalize_order(order, cart):
    for item in cart:
        product = item['product']
        product.stock -= item['quantity']
        product.save()
    cart.clear()