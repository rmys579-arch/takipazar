import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Proje dizini ayarları
BASE_DIR = Path(__file__).resolve().parent.parent

# GÜVENLİK AYARLARI
SECRET_KEY = 'django-insecure-ozel-anahtar-buraya-gelecek'
DEBUG = True # Kendi bilgisayarında hataları görmek için True olmalı
ALLOWED_HOSTS = [
    'www.takipazar.com.tr', 
    'takipazar.com.tr', 
    'rumsuls.pythonanywhere.com', 
    '127.0.0.1',
    'localhost'
]

# UYGULAMA TANIMLARI
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop.apps.ShopConfig', # Uygulama yapına göre güncellendi
    'cart.apps.CartConfig',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware', # Dil desteği için kritik
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gumus_projesi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Eğer dışarıda bir templates klasörün varsa
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'shop.context_processors.categories',
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

# VERİTABANI AYARLARI (PostgreSQL Bağlantısı)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'gumus.db',          # pgAdmin'de oluşturduğun veritabanı adı
        'USER': 'postgres',          # Kullanıcı adın
        'PASSWORD': '7Rec1623.',     # Kurulumda belirlediğin şifre
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

# DİL VE SAAT AYARLARI (Çoklu Dil Desteği)
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
    os.path.join(BASE_DIR, 'locale'),
]

# STATİK VE MEDYA DOSYALARI
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# DİĞER AYARLAR
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
CART_SESSION_ID = 'cart'

# E-posta Konfigürasyonu
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'rmys579@gmail.com'
DEFAULT_FROM_EMAIL = 'Takı Pazar <rmys579@gmail.com>'

# GÜVENLİK AYARLARI (Yerel testte False olmalı, canlıda True yapılır)
SECURE_SSL_REDIRECT = False  
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = ['https://www.takipazar.com.tr', 'https://takipazar.com.tr']
# Django'nun varsayılan aradığı yolu kendi yolunla değiştiriyoruz
LOGIN_URL = 'shop:login'
# Email Ayarları
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'rmys579@gmail.com' # Buraya kendi mailini yaz
EMAIL_HOST_PASSWORD = 'bjqposqoxooxgsown' # 16 haneli uygulama şifresi
DEFAULT_FROM_EMAIL = 'Takı Pazar <rmys579@gmail.com>'
