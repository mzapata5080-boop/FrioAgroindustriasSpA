from django.urls import path

from . import views
from .kardex_views import kardex

app_name = "inventario"

urlpatterns = [
    path("", views.stock, name="stock"),
    path("ingresos/", views.movimientos, {"seccion": "ingresos"}, name="ingresos"),
    path("salidas/", views.movimientos, {"seccion": "salidas"}, name="salidas"),
    path("kardex/", kardex, name="kardex"),
]