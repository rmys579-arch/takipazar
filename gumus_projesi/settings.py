import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Proje dizini ayarları
BASE_DIR = Path(__file__).resolve().parent.parent

# GÜVENLİK AYARLARI (Geliştirme aşamasında bunlar kalabilir)
SECRET_KEY = 'django-insecure-ozel-anahtar-buraya-gelecek'
DEBUG = False
ALLOWED_HOSTS = [
    'www.takipazar.com', 
    'takipazar.com', 
    'rumsuls.pythonanywhere.com', 
    '127.0.0.1'
]

# UYGULAMA TANIMLARI
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop', # Senin oluşturduğun ürün yönetim uygulaması
    'cart', # Sepet uygulaması
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', # Dil desteği için kritik
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gumus_projesi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'gumus_projesi.wsgi.application'

# VERİTABANI AYARLARI (PostgreSQL Bağlantısı)[cite: 2]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gumus.db',          # pgAdmin'de oluşturduğun veritabanı adı[cite: 2]
        'USER': 'postgres',          # Kullanıcı adın[cite: 2]
        'PASSWORD': '7Rec1623.',  # Kurulumda belirlediğin şifre[cite: 2]
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# ŞİFRE DOĞRULAMA
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# DİL VE SAAT AYARLARI (Çoklu Dil Desteği)[cite: 2]
LANGUAGE_CODE = 'tr'
TIME_ZONE = 'Europe/Istanbul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('tr', _('Turkish')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale/'),
]

# STATİK VE MEDYA DOSYALARI (Ürün resimleri için)[cite: 2]
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cart.apps.CartConfig',
    'shop.apps.ShopConfig',
]
import os
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# settings.py dosyasının en sonuna ekle

# Çıkış yaptıktan sonra yönlendirilecek adres (Ana sayfa)
# settings.py en altı
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGOUT_ON_GET = True
CART_SESSION_ID = 'cart'
# E-posta Konfigürasyonu
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'rmys579@gmail.com' # Kendi Gmail adresin
EMAIL_HOST_PASSWORD = 'iwgcfjdcvqiwrply' # Google'dan aldığın 16 haneli kod
DEFAULT_FROM_EMAIL = 'Takı Pazar <rmys579@gmail.com>'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
SECURE_SSL_REDIRECT = True  # Tüm trafiği HTTPS'e yönlendirir
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
CSRF_TRUSTED_ORIGINS = ['https://www.takipazar.com.tr', 'https://takipazar.com.tr']