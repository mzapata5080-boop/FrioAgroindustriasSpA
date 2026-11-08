from django.urls import path
from finanzas.views import *


urlpatterns = [

    path(
        "clientes/",
        ClienteListView.as_view(),
        name="cliente_list"
    ),

    # Crear cliente
    path(
        "clientes/nuevo/",
        ClienteCreateView.as_view(),
        name="cliente_create"
    ),

    # Editar cliente
    path(
        "clientes/editar/<int:pk>/",
        ClienteUpdateView.as_view(),
        name="cliente_edit"
    ),

    # Eliminar cliente
    path(
        "clientes/eliminar/<int:pk>/",
        ClienteDeleteView.as_view(),
        name="cliente_delete"
    ),
    # ver detalle de cliente
    path(
        "clientes/detalle/<int:pk>/",
        ClienteDetailView.as_view(),
        name="cliente_detail"
    ),
]