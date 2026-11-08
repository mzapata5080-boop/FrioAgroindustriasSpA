from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from finanzas.forms import ClienteForm
from .models import Cliente



class ClienteListView(ListView):
    """
    Muestra el listado completo
    de clientes registrados.
    """

    model = Cliente

    template_name = (
        "finanzas/clientes/listar.html"
    )

    context_object_name = "clientes"

class ClienteCreateView(CreateView):
    """
    Permite registrar nuevos clientes.
    """

    model = Cliente

    form_class = ClienteForm

    template_name = (
        "finanzas/clientes/crear.html"
    )

    success_url = reverse_lazy(
        "cliente_list"
    )

class ClienteUpdateView(UpdateView):
    """
    Permite modificar clientes existentes.
    """

    model = Cliente

    form_class = ClienteForm

    template_name = (
        "finanzas/clientes/editar.html"
    )

    success_url = reverse_lazy(
        "cliente_list"
    )

class ClienteDeleteView(DeleteView):
    """
    Permite eliminar clientes.
    """

    model = Cliente

    template_name = (
        "finanzas/clientes/eliminar.html"
    )

    success_url = reverse_lazy(
        "cliente_list"
    )

