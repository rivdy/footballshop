from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price", "is_featured", "stock", "brand", "created_at")
    list_filter = ("category", "is_featured", "brand")
    search_fields = ("name", "brand", "description")
    ordering = ("-created_at",)
