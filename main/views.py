from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from .models import Product
from .forms import ProductForm


def show_products(request):
    products = Product.objects.all().order_by('-created_at')
    context = {
        "app_name": "Garuda Football Shop",
        "student_name": "Rivaldy Putra Rivly",
        "student_class": "PBP B",
        "products": products,
    }
    return render(request, "product_list.html", context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})

def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():             # <- validasi form
            form.save()
            return redirect("main:product_list")
    else:
        form = ProductForm()
    return render(request, "product_form.html", {"form": form})

# ---- Data Delivery (JSON/XML) ----
def show_json(request):
    data = Product.objects.all()
    return HttpResponse(
        serializers.serialize("json", data),
        content_type="application/json"
    )

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(
        serializers.serialize("xml", data),
        content_type="application/xml"
    )

def show_json_by_id(request, pk):
    data = Product.objects.filter(pk=pk)
    return HttpResponse(
        serializers.serialize("json", data),
        content_type="application/json"
    )

def show_xml_by_id(request, pk):
    data = Product.objects.filter(pk=pk)
    return HttpResponse(
        serializers.serialize("xml", data),
        content_type="application/xml"
    )

def product_json(request):
    products = Product.objects.all()
    data = serializers.serialize("json", products)
    return HttpResponse(data, content_type="application/json")

def product_xml(request):
    products = Product.objects.all()
    data = serializers.serialize("xml", products)
    return HttpResponse(data, content_type="application/xml")

def product_json_by_id(request, pk):
    product = Product.objects.filter(pk=pk)
    data = serializers.serialize("json", product)
    return HttpResponse(data, content_type="application/json")

def product_xml_by_id(request, pk):
    product = Product.objects.filter(pk=pk)
    data = serializers.serialize("xml", product)
    return HttpResponse(data, content_type="application/xml")
