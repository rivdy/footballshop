from django.urls import path
from .views import (
    register, login_user, logout_user,
    show_products, product_detail, create_product,
    show_json, show_json_by_id, show_xml, show_xml_by_id,
    edit_product, delete_product, 
)

app_name = "main"

urlpatterns = [
    path("", show_products, name="show_products"),
    path("product/<int:id>/", product_detail, name="product_detail"),
    path("add/", create_product, name="create_product"),
    path("", show_products, name="home"),
    path("product/<int:pk>/edit/", edit_product, name="edit_product"),
    path("product/<int:pk>/delete/", delete_product, name="delete_product"),
    
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),

    path("json/", show_json, name="show_json"),
    path("json/<int:id>/", show_json_by_id, name="show_json_by_id"),
    path("xml/", show_xml, name="show_xml"),
    path("xml/<int:id>/", show_xml_by_id, name="show_xml_by_id"),
]
