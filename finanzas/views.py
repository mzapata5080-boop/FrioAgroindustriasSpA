from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from finanzas.forms import ClienteForm
from .models import Cliente
from django.views.generic import DetailView


from django.views.generic import ListView

from .models import Cliente


class ClienteListView(ListView):
    """
    Muestra el listado de clientes y
    el detalle del cliente seleccionado.
    """

    model = Cliente

    template_name = (
        "finanzas/clientes/listar.html"
    )

    context_object_name = "clientes"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        cliente_id = self.request.GET.get(
            "cliente"
        )

        if cliente_id:

            try:

                context["cliente_seleccionado"] = (
                    Cliente.objects.get(
                        id=cliente_id
                    )
                )

            except Cliente.DoesNotExist:

                context["cliente_seleccionado"] = None

        return context


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

class ClienteDetailView(DetailView):
    """
    Muestra los detalles
    completos de un cliente.
    """

    model = Cliente

    template_name = (
        "finanzas/clientes/detalle.html"
    )

    context_object_name = (
        "cliente"
    )