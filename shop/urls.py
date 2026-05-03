# shop/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'shop'

urlpatterns = [
    # 1. Ana Sayfa
    path('', views.product_list, name='product_list'),
    
    # 2. Üyelik ve Kullanıcı İşlemleri
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # 3. Ürün Detay Yolları (Kritik Çözüm)
    # Eğer slug boşsa bu yol çalışır ve NoReverseMatch hatasını engeller
    path('<int:id>/', views.product_detail, name='product_detail_simple'), 
    # Slug doluysa standart bu yol çalışır
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('checkout/', views.order_create, name='order_create'),
    # 4. Kategori Filtreleme Yolu (En sonda olmalı)
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    
]