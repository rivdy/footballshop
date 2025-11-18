from django.urls import path
from .views import (
    # auth halaman web
    register,
    login_user,
    logout_user,

    # halaman utama
    show_products,
    product_detail,
    create_product,
    edit_product,
    delete_product,
    home,
    product_list,

    # JSON/XML
    show_json,
    show_json_by_id,
    show_xml,
    show_xml_by_id,

    # AJAX (Tugas 6)
    products_json,
    product_create_ajax,
    product_update_ajax,
    product_delete_ajax,
    login_ajax,
    register_ajax,
    logout_ajax,

    # API Flutter (Tugas 9)
    products_flutter,
    product_detail_flutter,
)

app_name = "main"

urlpatterns = [
    # ====== AUTH HALAMAN WEB ======
    path("login/", login_user, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout_user, name="logout"),

    # ====== HALAMAN BIASA ======
    path("", show_products, name="show_products"),
    path("home/", home, name="home"),
    path("product/<int:id>/", product_detail, name="product_detail"),
    path("add/", create_product, name="create_product"),
    path("product/<int:id>/edit/", edit_product, name="edit_product"),
    path("product/<int:id>/delete/", delete_product, name="delete_product"),
    path("products/page/", product_list, name="product_list"),

    # ====== JSON / XML ======
    path("json/", show_json, name="show_json"),
    path("json/<int:id>/", show_json_by_id, name="show_json_by_id"),
    path("xml/", show_xml, name="show_xml"),
    path("xml/<int:id>/", show_xml_by_id, name="show_xml_by_id"),

    # ====== AJAX (TUGAS 6) ======
    path("ajax/products/", products_json, name="products_json"),
    path("ajax/products/create/", product_create_ajax, name="product_create_ajax"),
    path("ajax/products/<int:id>/update/", product_update_ajax, name="product_update_ajax"),
    path("ajax/products/<int:id>/delete/", product_delete_ajax, name="product_delete_ajax"),

    path("ajax/login/", login_ajax, name="login_ajax"),
    path("ajax/register/", register_ajax, name="register_ajax"),
    path("ajax/logout/", logout_ajax, name="logout_ajax"),

    # ====== API UNTUK FLUTTER (TUGAS 9) ======
    path("api/flutter/products/", products_flutter, name="products_flutter"),
    path(
        "api/flutter/products/<int:id>/",
        product_detail_flutter,
        name="product_detail_flutter",
    ),
]
