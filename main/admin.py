from django.contrib import admin
from django.contrib import admin
from .models import Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','category','is_featured','stock','brand','rating')
    list_filter  = ('category','is_featured','brand')
    search_fields = ('name','brand','description')
# Register your models here.
