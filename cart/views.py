from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from shop.forms import OrderCreateForm

# cart/views.py dosyandaki cart_add fonksiyonunu bu şekilde güncelle:

# cart/views.py içindeki cart_add fonksiyonu:

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Formdan gelen değeri al ve sayıya çevir
    try:
        qty = int(request.POST.get('quantity', 1))
    except ValueError:
        qty = 1
        
    mode = request.POST.get('mode', 'perakende')
    
    # Ürünü ekle/güncelle
    cart.add(product=product, quantity=qty, mode=mode)
    
    return redirect('cart:cart_detail')
def cart_remove(request, product_id):
    """Ürünü sepetten çıkaran fonksiyon."""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    """Sepet sayfasını görüntüleyen fonksiyon."""
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})
# cart/views.py dosyasının en altına ekle
import urllib.parse

def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        # Formdan gelen müşteri bilgileri
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        # WhatsApp mesajını oluşturma
        message = f"Merhaba NUVE! Yeni bir siparişim var:\n\n"
        message += f"👤 *Müşteri:* {name}\n"
        message += f"📞 *Telefon:* {phone}\n"
        message += f"📍 *Adres:* {address}\n\n"
        message += f"🛒 *Sipariş Detayı:*\n"
        
        for item in cart:
            message += f"- {item['quantity']} adet {item['product'].name} ({item['mode']}) - {item['total_price']} TL\n"
            
        message += f"\n💰 *GENEL TOPLAM:* {cart.get_total_price()} TL"
        
        # Mesajı URL formatına çeviriyoruz
        encoded_message = urllib.parse.quote(message)
        
        # Kendi telefon numaranı buraya yaz (Örn: 905301234567)
        whatsapp_url = f"https://wa.me/90XXXXXXXXXX?text={encoded_message}"
        
        # Siparişi gönderdikten sonra sepeti temizleyelim
        cart.clear()
        
        return redirect(whatsapp_url)
        
    return render(request, 'cart/checkout.html', {'cart': cart})
from shop.models import Order

def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        # Form verilerini alıyoruz
        order = Order.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            country_code=request.POST.get('country_code'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            total_paid=cart.get_total_price(),
            email=request.POST.get('email'),
        )
        
        # Sipariş numarasını template'e göndermek için değişkene alalım
        order_no = order.order_number
        cart.clear()
        return render(request, 'cart/order_success.html', {'order_no': order_no})
        
    return render(request, 'shop/checkout.html', {'cart': cart} )