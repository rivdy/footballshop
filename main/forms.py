from django import forms
from .models import Product
from django.forms import ModelForm
from main.models import Product
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'price', 'description', 'thumbnail',
            'category', 'is_featured', 'stock'
        ]
