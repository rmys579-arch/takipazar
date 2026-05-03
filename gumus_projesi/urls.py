# gumus_projesi/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static

# 1. Dil bağımsız yollar (Dil kodu gerektirmeyenler)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')), # Dil değiştirme fonksiyonu için şart
]

# 2. Dil bağımlı yollar (Başına /tr/ veya /en/ alanlar)
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('', include('shop.urls', namespace='shop')),
)

# 3. Geliştirme modunda medya ve statik dosyaları görünür kılar
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)