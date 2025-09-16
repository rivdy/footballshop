# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.core import serializers

from .models import Product
from .forms import ProductForm


def show_products(request):
    products = Product.objects.all().order_by("-created_at")
    context = {"products": products}
    return render(request, "product_list.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})


def create_product(request):
    """
    Form tambah produk.
    NOTE: kalau templatenya bernama 'create_news.html', tetap dipakai di sini.
    """
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("main:home")
    else:
        form = ProductForm()
    return render(request, "create_news.html", {"form": form})


# ---------- Data Delivery (untuk Postman) ----------

def products_json(request):
    qs = Product.objects.all()
    data = serializers.serialize("json", qs)
    return HttpResponse(data, content_type="application/json")


def product_json_by_id(request, id):
    qs = Product.objects.filter(pk=id)
    if not qs.exists():
        return HttpResponseNotFound(f'{{"detail":"Product {id} not found"}}')
    data = serializers.serialize("json", qs)
    return HttpResponse(data, content_type="application/json")


def products_xml(request):
    qs = Product.objects.all()
    data = serializers.serialize("xml", qs)
    return HttpResponse(data, content_type="application/xml")


def product_xml_by_id(request, id):
    qs = Product.objects.filter(pk=id)
    if not qs.exists():
        return HttpResponseNotFound("<error>Not Found</error>", content_type="application/xml")
    data = serializers.serialize("xml", qs)
    return HttpResponse(data, content_type="application/xml")
# --- alias agar cocok dengan urls lama ---
def show_json(request):
    return products_json(request)

def show_json_by_id(request, id):
    return product_json_by_id(request, id)

def show_xml(request):
    return products_xml(request)

def show_xml_by_id(request, id):
    return product_xml_by_id(request, id)
