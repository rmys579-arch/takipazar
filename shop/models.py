from decimal import Decimal
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.auth.models import User 

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("Kategori Adı"))
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"

    # Meta bloğunun DIŞINDA ve onunla AYNI HİZADA olmalı
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, verbose_name=_("Ürün Adı"))
    description = models.TextField(verbose_name=_("Açıklama"))
    weight = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_("Gram Ağırlığı"))
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("İşçilik Bedeli"))
    price_retail = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Perakende Fiyat"))
    price_wholesale = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Toptan Fiyat"))
    image = models.ImageField(upload_to='products/', verbose_name=_("Ürün Görseli"))
    stock = models.PositiveIntegerField(default=0, verbose_name=_("Stok Adedi"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"

    # Meta bloğunun DIŞINDA ve onunla AYNI HİZADA olmalı
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id])

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_wholesaler = models.BooleanField(default=False, verbose_name="Toptancı mı?")
    company_name = models.CharField(max_length=200, blank=True, verbose_name="Firma Adı")

    def __str__(self):
        return f"{self.user.username} - {self.company_name}"

class Order(models.Model):
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    country_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Turkey')
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Hazırlanıyor')
    gift_wrap = models.BooleanField(default=False)
    gift_note = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"TP-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sipariş {self.order_number}"

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    name = models.CharField(max_length=50) 
    value = models.CharField(max_length=50) 
    extra_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.product.name} - {self.name}: {self.value}"

class Newsletter(models.Model):
    email = models.EmailField(unique=True, verbose_name="E-posta Adresi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Kayıt Tarihi")

    class Meta:
        verbose_name = "Bülten Abonesi"
        verbose_name_plural = "Bülten Aboneleri"

    def __str__(self):
        return self.email