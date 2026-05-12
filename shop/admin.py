from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from django.utils.html import format_html
from import_export import resources
from .models import Order, Category, Product, Variation

# Excel Yapısı
class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'price_retail', 'price_wholesale', 'stock', 'description')
        import_id_fields = ('id',)

# Varyasyon Tablosu
class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1
    verbose_name = "Varyasyon"
    verbose_name_plural = "Varyasyonlar"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # BURASI KRİTİK: Sadece 'asef_fedex_button' olmalı, 'dhl_label_button' SİLİNDİ.
    list_display = ['order_number', 'first_name', 'last_name', 'city', 'status', 'total_paid', 'asef_fedex_button']
    
    def asef_fedex_button(self, obj):
        # FedEx Moru (#4D148C) ile şık bir buton
        return format_html(
            '<a class="button" style="background-color:#4D148C; color:white; padding:5px 10px; border-radius:4px; font-weight:bold; text-decoration:none;" '
            'href="https://www.fedex.com/fedextrack/?trknbr={}" target="_blank">ASEF / FedEx Takip</a>',
            obj.order_number
        )
    asef_fedex_button.short_description = "Kargo İşlemi"

@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_display = ['name', 'price_retail', 'stock', 'category']
    inlines = [VariationInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# Admin Paneli Başlıklarını Türkçeleştirme
admin.site.site_header = "Takı Pazar Yönetim Paneli"
admin.site.site_title = "Takı Pazar Admin"
admin.site.index_title = "Yönetim Paneline Hoş Geldiniz"