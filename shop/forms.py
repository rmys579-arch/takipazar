from django import forms
from .models import Order
from django.utils.translation import gettext_lazy as _

class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(label=_("Adınız"))
    last_name = forms.CharField(label=_("Soyadınız"))
    email = forms.EmailField(label=_("E-posta"))
    phone = forms.CharField(label=_("Telefon"))

    address = forms.CharField(label=_("Adres"))
    city = forms.CharField(label=_("Şehir"))
    country_code = forms.CharField(
        initial='+90', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+90', 'style': 'width: 80px;'})
    )
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'address', 'city', 'zip_code', 'country', 'gift_wrap', 'gift_note'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Adınız'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Soyadınız'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-posta'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+90...'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Açık Adres'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Şehir'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Posta Kodu'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ülke'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '5xx xxx xx xx'}),
            'gift_note': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Hediye notunuz...'}),
        }
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Mevcut OrderCreateForm kodların burada kalsın...

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_("E-posta Adresi"))

    class Meta:
        model = User
        fields = ("username", "email")
        labels = {
            'username': _("Kullanıcı Adı"),
            'email': _("E-posta Adresi"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control' # Bootstrap şıklığı için