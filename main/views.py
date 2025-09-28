# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

from .models import Product
from .forms import ProductForm

# ---------- Auth ----------
def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been successfully created!")
            return redirect("main:login")
    return render(request, "register.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # set cookie last_login
            response = HttpResponseRedirect(reverse("main:show_products"))
            response.set_cookie("last_login", str(datetime.datetime.now()))
            return response
    else:
        form = AuthenticationForm(request)
    return render(request, "login.html", {"form": form})

def logout_user(request):
    logout(request)
    resp = HttpResponseRedirect(reverse('main:login'))
    resp.delete_cookie('last_login')
    return resp

# ---------- Main & Detail ----------
@login_required(login_url="/login/")
def show_products(request):
    # ?filter=all (default) | ?filter=my
    filter_type = request.GET.get("filter", "all")
    if filter_type == "my":
        products = Product.objects.filter(user=request.user).order_by("id")
    else:
        products = Product.objects.all().order_by("id")

    context = {
        "npm": "2406351453",
        "name": request.user.username,
        "class": "PBP B",
        "products": products,
        "last_login": request.COOKIES.get("last_login", "Never"),
    }
    return render(request, "product_list.html", context)

@login_required(login_url="/login/")
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, "product_detail.html", {"product": product})

@login_required(login_url="/login/")
def create_product(request):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user  # hubungkan ke user yang login
        obj.updated_by = request.user
        obj.save()
        return redirect("main:show_products")
    return render(request, "create_product.html", {"form": form})
@login_required(login_url="/login/")
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == "POST":
        obj = form.save(commit=False)
        obj.updated_by = request.user     # catat editor terakhir
        obj.save()
        return redirect("main:product_detail", id=product.id)
    return render(request, "edit_product.html", {"form": form, "product": product})

# ---------- Bukti JSON/XML ----------
def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")
