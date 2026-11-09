from django.urls import path
from .views import (
    TrabajadorListView,
    TrabajadorCreateView,
    TrabajadorUpdateView,
    TrabajadorDeleteView
)

urlpatterns = [
    path('', TrabajadorListView.as_view(), name='trabajador_list'),
    path('crear/', TrabajadorCreateView.as_view(), name='trabajador_create'),
    path('editar/<int:pk>/', TrabajadorUpdateView.as_view(), name='trabajador_update'),
    path('eliminar/<int:pk>/', TrabajadorDeleteView.as_view(), name='trabajador_delete'),
]