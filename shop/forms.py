from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    country_code = forms.CharField(
        initial='+90', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+90', 'style': 'width: 80px;'})
    )
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone', 
            'address', 'city', 'zip_code', 'country'
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
        }