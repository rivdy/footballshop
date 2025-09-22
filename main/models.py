
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    CATEGORY_CHOICES = [
        ("jersey", "Jersey"),
        ("sepatu", "Sepatu"),
        ("aksesoris", "Aksesoris"),
        ("bola", "Bola"),
        ("lainnya", "Lainnya"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # tambahkan ini
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField(blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default="lainnya")
    is_featured = models.BooleanField(default=False)

    # tambahkan timestamp
    created_at = models.DateTimeField(auto_now_add=True)   # tadi sudah dimigrasi
    updated_at = models.DateTimeField(auto_now=True)

    # (opsional) atribut tambahan
    stock = models.IntegerField(default=0)
    brand = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} — Rp{self.price:,}"
