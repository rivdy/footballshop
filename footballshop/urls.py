"""
URL configuration for footballshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.http import HttpResponse

def ping(_):
    return HttpResponse("OK", content_type="text/plain")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__ping/", ping),  # cek cepat di PWS: /__ping/ harus "OK"
    path("", include("main.urls")),  # root diarahkan ke urls-nya app main
    # fallback kalau include di atas tidak memetakan root:
    path("", RedirectView.as_view(pattern_name="main:product_list", permanent=False)),
]


