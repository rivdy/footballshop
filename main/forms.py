from django import forms
from .models import Product
from django.forms import ModelForm
from main.models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("Username sudah terpakai.")
        return username

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'price', 'description', 'thumbnail',
            'category', 'is_featured', 'stock'
        ]
