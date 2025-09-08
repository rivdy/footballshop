from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('jersey', 'Jersey'),
        ('boots', 'Sepatu Bola'),
        ('ball', 'Bola'),
        ('accessories', 'Aksesori'),
        ('others', 'Lainnya'),
    ]

    # --- 6 atribut wajib ---
    name        = models.CharField(max_length=200)
    price       = models.IntegerField()
    description = models.TextField()
    thumbnail   = models.URLField()
    category    = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    is_featured = models.BooleanField(default=False)

    stock  = models.PositiveIntegerField(default=0)
    brand  = models.CharField(max_length=100, blank=True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} ({self.category})"
