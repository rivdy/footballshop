from django.urls import path
from .views import (
    # Halaman existing
    register, login_user, logout_user,
    show_products, product_detail, create_product,
    show_json, show_json_by_id, show_xml, show_xml_by_id,
    edit_product, delete_product,

    # ====== AJAX (Tugas 6) ======
    products_json,               # GET list products (with ?filter=all|my)
    product_create_ajax,         # POST create
    product_update_ajax,         # POST/PATCH update
    product_delete_ajax,         # POST/DELETE delete
    login_ajax,                  # POST login
    register_ajax,               # POST register
    logout_ajax,                 # POST logout
)

app_name = "main"

urlpatterns = [
    # ====== Halaman biasa ======
    path("", show_products, name="show_products"),
    path("product/<int:id>/", product_detail, name="product_detail"),
    path("add/", create_product, name="create_product"),
    path("", show_products, name="home"),  # alias (opsional)
    path("product/<int:id>/edit/", edit_product, name="edit_product"),
    path("product/<int:id>/delete/", delete_product, name="delete_product"),

    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),

    path("json/", show_json, name="show_json"),
    path("json/<int:id>/", show_json_by_id, name="show_json_by_id"),
    path("xml/", show_xml, name="show_xml"),
    path("xml/<int:id>/", show_xml_by_id, name="show_xml_by_id"),

    # ====== AJAX (Tugas 6) ======
    path("ajax/products/", products_json, name="products_json"),                      # GET
    path("ajax/products/create/", product_create_ajax, name="product_create_ajax"),   # POST
    path("ajax/products/<int:id>/update/", product_update_ajax, name="product_update_ajax"),  # POST/PATCH
    path("ajax/products/<int:id>/delete/", product_delete_ajax, name="product_delete_ajax"),  # POST/DELETE

    path("ajax/login/", login_ajax, name="login_ajax"),            # POST
    path("ajax/register/", register_ajax, name="register_ajax"),   # POST
    path("ajax/logout/", logout_ajax, name="logout_ajax"),         # POST
    path("ajax/products/", products_json, name="products_json"),
    path("ajax/products/create/", product_create_ajax, name="product_create_ajax"),
    path("ajax/products/<int:id>/update/", product_update_ajax, name="product_update_ajax"),
    path("ajax/products/<int:id>/delete/", product_delete_ajax, name="product_delete_ajax"),
    path("ajax/login/", login_ajax, name="login_ajax"),
    path("ajax/register/", register_ajax, name="register_ajax"),
    path("ajax/logout/", logout_ajax, name="logout_ajax"),

]
