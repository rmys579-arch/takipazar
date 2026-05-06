# shop/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'shop'

urlpatterns = [
    # 1. Sabit Sayfalar
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('track-order/', views.track_order, name='track_order'),
    path('faq/', views.faq, name='faq'),
    path('return-policy/', views.return_policy, name='return_policy'), # Hata buradaydı
    path('checkout-options/', views.checkout_gateway, name='checkout_gateway'),
    path('checkout/', views.order_create, name='order_create'),

    # 2. Üyelik İşlemleri
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # 3. Ürün Detay
    path('<int:id>/', views.product_detail, name='product_detail_simple'), 
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    # 4. Diğer Dinamik İşlemler
    path('subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'), # Üste aldık
    
    # 5. Kategori Yolu (MUTLAKA EN SONDA)
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
]