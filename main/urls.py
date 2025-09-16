from django.urls import path
from .views import (
    show_products, product_detail, create_product,
    show_json, show_json_by_id, show_xml, show_xml_by_id,
)

app_name = "main"

urlpatterns = [
    path("", show_products, name="product_list"),            # ROOT /
    path("add/", create_product, name="create_product"),
    path("product/<int:pk>/", product_detail, name="product_detail"),

    # Data delivery endpoints (Tugas 3)
    path("json/", show_json, name="show_json"),
    path("json/<int:id>/", show_json_by_id, name="show_json_by_id"),
    path("xml/", show_xml, name="show_xml"),
    path("xml/<int:id>/", show_xml_by_id, name="show_xml_by_id"),
]
