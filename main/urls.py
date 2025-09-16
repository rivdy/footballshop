from django.urls import path
from .views import (
    show_products,           # <- daftar produk (home)
    product_detail,
    create_product,
    show_json,
    show_json_by_id,
    show_xml,
    show_xml_by_id,
)

app_name = "main"

urlpatterns = [
    path("", show_products, name="home"),
    path("add/", create_product, name="create_product"),
    path("product/<int:pk>/", product_detail, name="product_detail"),
    path("json/", show_json, name="json"),
    path("json/<int:id>/", show_json_by_id, name="json_by_id"),
    path("xml/", show_xml, name="xml"),
    path("xml/<int:id>/", show_xml_by_id, name="xml_by_id"),
]
