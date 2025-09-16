from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.show_products, name="product_list"),
    path("add/", views.create_product, name="product_add"),
    path("product/<int:pk>/", views.product_detail, name="product_detail"),

    # data delivery
    path("json/", views.show_json, name="json"),
    path("xml/", views.show_xml, name="xml"),
    path("json/<int:pk>/", views.show_json_by_id, name="json_by_id"),
    path("xml/<int:pk>/", views.show_xml_by_id, name="xml_by_id"),
]
