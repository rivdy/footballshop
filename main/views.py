# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
from django.db import IntegrityError
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt


# ---------- Auth ----------
def product_to_dict(p: Product):
    return {
        "id": p.id,
        "name": p.name,
        "price": int(p.price) if getattr(p, "price", None) is not None else 0,
        "description": getattr(p, "description", "") or "",
        "category": getattr(p, "category", "") or "",
        "thumbnail": getattr(p, "thumbnail", "") or "",
        "is_featured": bool(getattr(p, "is_featured", False)),
        "owner": getattr(getattr(p, "user", None), "username", None),
        "created_at": getattr(p, "created_at", None).isoformat() if getattr(p, "created_at", None) else None,
        "updated_at": getattr(p, "updated_at", None).isoformat() if getattr(p, "updated_at", None) else None,
    }
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Akun berhasil dibuat. Silakan login.")
                return redirect("main:login")
            except IntegrityError:
                form.add_error("username", "Username sudah dipakai.")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        # PENTING: sertakan 'request' di argumen pertama
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # set cookie last_login (format rapi, tanpa spasi nyasar)
            response = HttpResponseRedirect(reverse("main:show_products"))
            response.set_cookie("last_login", timezone.now().strftime("%Y-%m-%d %H:%M"))
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
    # === Filter dasar ===
    filter_type = request.GET.get("filter", "all")  # "all" | "my"

    qs = Product.objects.all().select_related("user").order_by("-created_at")
    if filter_type == "my":
        qs = qs.filter(user=request.user)
    last_login_raw = request.COOKIES.get("last_login") or ""
    last_login_fmt = last_login_raw[:16] if last_login_raw else "Never"  # YYYY-mm-dd HH:MM

    # === Pagination: 4 produk per halaman ===
    paginator = Paginator(qs, 4)
    page_number = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "npm": "2406351453",
        "name": request.user.username,
        "class": "PBP B",
        "products": page_obj,  # kirim Page object (bukan queryset mentah)
        "filter_type": filter_type,
        "last_login": last_login_fmt,
        "total_items": paginator.count,
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
@login_required
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.user != request.user and not request.user.is_staff:
        return redirect('main:show_products')

    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        obj = form.save(commit=False)
        # opsional: catat editor
        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user
        obj.save()
        return redirect('main:product_detail', id=product.id)

    return render(request, "edit_product.html", {"form": form})

@login_required
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.user != request.user and not request.user.is_staff:
        return redirect('main:show_products')

    if request.method == "POST":
        product.delete()
        return redirect('main:show_products')

    # konfirmasi sederhana (boleh skip & langsung pakai tombol form POST di kartu)
    return render(request, "confirm_delete.html", {"product": product})
@login_required
def home(request):
    last_login_cookie = request.COOKIES.get('last_login')  # None jika tidak ada
    return render(request, 'main/home.html', {
        'last_login_cookie': last_login_cookie,
        'last_login_user': getattr(request.user, 'last_login', None),  # dari DB/session
    })
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

def product_list(request):
    qs = Product.objects.all().order_by('-created_at')
    paginator = Paginator(qs, 4)  # <= 4 produk per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main.html', {'products': page_obj})  # ganti context key jika perlu
# ===================== AJAX (TUGAS 6) =====================

# ---- LIST PRODUCTS (GET) ----
@login_required(login_url="/login/")
@require_http_methods(["GET"])
def products_json(request):
    scope = request.GET.get("filter", "all")  # "all" | "my"
    qs = Product.objects.all().order_by("-created_at")
    if scope == "my":
        qs = qs.filter(user=request.user)

    items = [product_to_dict(p) for p in qs]
    return JsonResponse({"ok": True, "count": len(items), "items": items}, status=200)


# ---- CREATE PRODUCT (POST) ----
@csrf_exempt
@login_required(login_url="/login/")
@require_http_methods(["POST", "PATCH"])
def product_create_ajax(request):
    form = ProductForm(request.POST, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # pastikan ownership tercatat
        if hasattr(obj, "user"):
            obj.user = request.user
        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user
        if hasattr(obj, "created_at") and getattr(obj, "created_at") is None:
            obj.created_at = timezone.now()
        obj.save()
        return JsonResponse({"ok": True, "item": product_to_dict(obj)}, status=201)
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)


# ---- UPDATE PRODUCT (POST/PATCH) ----
@login_required(login_url="/login/")
@require_http_methods(["POST", "PATCH"])
def product_update_ajax(request, id):
    product = get_object_or_404(Product, pk=id)

    # izin: owner atau staff
    if getattr(product, "user", None) != request.user and not request.user.is_staff:
        return JsonResponse({"ok": False, "error": "Forbidden"}, status=403)

    form = ProductForm(request.POST, request.FILES or None, instance=product)
    if form.is_valid():
        obj = form.save(commit=False)
        if hasattr(obj, "updated_by"):
            obj.updated_by = request.user
        obj.save()
        return JsonResponse({"ok": True, "item": product_to_dict(obj)}, status=200)
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)


# ---- DELETE PRODUCT (POST/DELETE) ----
@csrf_exempt
@login_required(login_url="/login/")
@require_http_methods(["POST", "DELETE"])
def product_delete_ajax(request, id):
    product = get_object_or_404(Product, pk=id)

    # izin: owner atau staff
    if getattr(product, "user", None) != request.user and not request.user.is_staff:
        return JsonResponse({"ok": False, "error": "Forbidden"}, status=403)

    product.delete()
    return JsonResponse({"ok": True}, status=200)


# ---- LOGIN (POST) ----
@require_http_methods(["POST"])
def login_ajax(request):
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        # Atau gunakan authenticate(...) jika mau manual:
        # user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(request, user)
            resp = JsonResponse({"ok": True, "user": user.username}, status=200)
            # set cookie last_login (format rapi)
            resp.set_cookie("last_login", timezone.now().strftime("%d %b %Y, %H:%M"))
            return resp
    # error
    return JsonResponse({"ok": False, "errors": form.errors or {"__all__": ["Invalid credentials"]}}, status=400)


# ---- REGISTER (POST) ----
@require_http_methods(["POST"])
def register_ajax(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        return JsonResponse({"ok": True, "user": user.username}, status=201)
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)


# ---- LOGOUT (POST) ----
@login_required(login_url="/login/")
@require_http_methods(["POST"])
def logout_ajax(request):
    logout(request)
    resp = JsonResponse({"ok": True}, status=200)
    resp.delete_cookie("last_login")
    return resp
# ===================== API UNTUK FLUTTER (TUGAS 9) =====================

@login_required(login_url="/login/")
@require_http_methods(["GET"])
def products_flutter(request):
    """
    Endpoint LIST untuk Flutter.
    - Jika query ?filter=my  => hanya produk milik user login
    - Jika tidak ada / filter=all => semua produk
    Response: list of product_to_dict(...)
    """
    scope = request.GET.get("filter", "all")  # "all" | "my"

    qs = Product.objects.all().select_related("user").order_by("-created_at")
    if scope == "my":
        qs = qs.filter(user=request.user)

    data = [product_to_dict(p) for p in qs]
    # Contoh JSON (list):
    # [
    #   {"id": 1, "name": "...", "price": 100000, ...},
    #   ...
    # ]
    return JsonResponse(data, safe=False, status=200)


@login_required(login_url="/login/")
@require_http_methods(["GET"])
def product_detail_flutter(request, id):
    """
    Endpoint DETAIL untuk Flutter.
    Mengembalikan satu produk dalam bentuk JSON flat.
    """
    product = get_object_or_404(Product, pk=id)

    # Opsional: batasi hanya owner atau staff
    # if getattr(product, "user", None) != request.user and not request.user.is_staff:
    #     return JsonResponse({"detail": "Forbidden"}, status=403)

    return JsonResponse(product_to_dict(product), status=200)
