"""
URL configuration for footballshop project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
    path("auth/", include("authentication.urls")),  # endpoint login/register untuk Flutter
    
]
