from django.urls import path
from .views import show_home

app_name = "main"
urlpatterns = [ path("", show_home, name="show_home") ]
