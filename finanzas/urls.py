from django.urls import path
from . import views

from django.urls import path
from .views import *

urlpatterns = [
    # Rutas del módulo de Proveedores
    path('proveedores/', views.proveedor_list, name='proveedor_list'),
    path('proveedores/nuevo/', views.proveedor_create, name='proveedor_create'),
    path('proveedores/editar/<int:pk>/', views.proveedor_update, name='proveedor_update'),
    path('proveedores/eliminar/<int:pk>/', views.proveedor_delete, name='proveedor_delete'),
    
    # Rutas del módulo de Facturas de Compra
    path('facturas/nueva/',FacturaCreateView.as_view(),name='factura_create'),
    
    # CLIENTES
    
        path(
            'clientes/',
            ClienteListView.as_view(),
            name='cliente_list'
        ),
    
        path(
            'clientes/nuevo/',
            ClienteCreateView.as_view(),
            name='cliente_create'
        ),
    
        path(
            'clientes/editar/<int:pk>/',
            ClienteUpdateView.as_view(),
            name='cliente_edit'
        ),
    
        path(
            'clientes/eliminar/<int:pk>/',
            ClienteDeleteView.as_view(),
            name='cliente_delete'
        ),
    
        path(
            'clientes/detalle/<int:pk>/',
            ClienteDetailView.as_view(),
            name='cliente_detail'
        ),
    
]

