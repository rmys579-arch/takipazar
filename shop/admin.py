from import_export.admin import ImportExportModelAdmin # Yeni eklendi
from django.contrib import admin
from django.utils.html import format_html
from import_export import resources # Yeni eklendi
from .models import Order, Category, Product, Variation

# Karakter temizleyici (DHL ve global sistemler için)
def turkish_to_english(text):
    if not text:
        return ""
    chars = str.maketrans("ğĞçÇşŞüÜöÖıİ", "gGcCsSuUoOiI") 
    return text.translate(chars)

# --- Excel Yapısı İçin Kaynak Sınıfı ---
class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        # Excel'de hangi sütunların olacağını belirliyoruz
        fields = ('id', 'name', 'category', 'price_retail', 'price_wholesale', 'stock', 'description')
        import_id_fields = ('id',)

# --- Varyasyon Tablosu Yapısı ---
class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1
    verbose_name = "Varyasyon"
    verbose_name_plural = "Varyasyonlar"
    fields = ['name', 'value', 'extra_price'] 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'first_name', 'last_name', 'city', 'status', 'total_paid', 'dhl_label_button']
    
    def dhl_label_button(self, obj):
        label_title = "TAKI PAZAR"
        customer_name = turkish_to_english(f"{obj.first_name} {obj.last_name}")
        clean_address = turkish_to_english(obj.address)
        clean_city = turkish_to_english(obj.city)
        barcode_url = f"https://bwipjs-api.metafloor.com/?bcid=code128&text={obj.order_number}&scale=2&includetext"
        
        label_content = f"""
        <div style='font-family:Arial; width:300px; border:2px solid #000; padding:15px; color:#000;'>
            <div style='text-align:center; border-bottom:1px solid #000; margin-bottom:10px;'>
                <h3>{label_title}</h3>
                <small>INTERNATIONAL SHIPPING</small>
            </div>
            <p><strong>TO:</strong> {customer_name}</p>
            <p><strong>ADDR:</strong> {clean_address}</p>
            <p><strong>CITY:</strong> {clean_city} / {obj.zip_code}</p>
            <p><strong>COUNTRY:</strong> {obj.country.upper()}</p>
            <p><strong>TEL:</strong> {obj.phone}</p>
            <hr>
            <div style='text-align:center;'><img src='{barcode_url}' style='width:100%'><p>No: {obj.order_number}</p></div>
        </div>
        """
        return format_html('''<a class="button" style="background-color:#d40511; color:white; padding:5px 10px; border-radius:4px; cursor:pointer;" onclick="var win = window.open('', '', 'width=400,height=600'); win.document.write('<html><body>' + `{}` + '</body></html>'); win.document.close(); setTimeout(function(){{ win.print(); }}, 500);">DHL Etiketi</a>''', label_content)

@admin.register(Product)
# ModelAdmin yerine ImportExportModelAdmin kullanarak Excel butonlarını ekledik
class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource # Excel şablonunu bağladık
    list_display = ['name', 'price_retail', 'stock', 'category']
    inlines = [VariationInline]
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:50px; height:50px; border-radius:5px;" />', obj.image.url)
        return "Görsel Yok"
    image_tag.short_description = 'Ürün Görseli'
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']