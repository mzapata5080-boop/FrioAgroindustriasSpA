from django.urls import path

from . import views
from .articulos_views import crear_articulo
from .ingresos_views import registrar_ingreso
from .kardex_views import kardex

app_name = "inventario"

urlpatterns = [
    path("", views.stock, name="stock"),
    path("articulos/nuevo/", crear_articulo, name="crear_articulo"),
    path("ingresos/", views.movimientos, {"seccion": "ingresos"}, name="ingresos"),
    path("ingresos/registrar/", registrar_ingreso, name="registrar_ingreso"),
    path("salidas/", views.movimientos, {"seccion": "salidas"}, name="salidas"),
    path("kardex/", kardex, name="kardex"),
]