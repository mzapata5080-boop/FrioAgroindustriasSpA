from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Proveedor, Cliente
from finanzas.forms import ProveedorForm, ClienteForm

from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.views.generic import DetailView
from .models import FacturaCompra
from .forms import FacturaCompraForm

@login_required
def proveedor_list(request):
    proveedores = Proveedor.objects.all().order_by('-creado_el')
    return render(request, 'finanzas/proveedor_list.html', {'proveedores': proveedores})

@login_required
def proveedor_create(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor registrado con éxito.')
            return redirect('proveedor_list')
    else:
        form = ProveedorForm()
    return render(request, 'finanzas/proveedor_form.html', {'form': form, 'titulo': 'Nuevo Proveedor'})

@login_required
def proveedor_update(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado.')
            return redirect('proveedor_list')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'finanzas/proveedor_form.html', {'form': form, 'titulo': 'Editar Proveedor'})

@login_required
def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado.')
        return redirect('proveedor_list')
    return render(request, 'finanzas/proveedor_confirm_delete.html', {'proveedor': proveedor})


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

    model = Cliente
    form_class = ClienteForm
    template_name = "finanzas/clientes/crear.html"
    success_url = reverse_lazy("cliente_list")

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

class ClienteUpdateView(UpdateView):

    model = Cliente
    form_class = ClienteForm
    template_name = "finanzas/clientes/editar.html"
    success_url = reverse_lazy("cliente_list")

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

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

class FacturaCreateView(CreateView):
    """
    Registrar nuevas facturas de compra.
    """

    model = FacturaCompra

    form_class = FacturaCompraForm

    template_name = (
        "finanzas/facturas/crear.html"
    )

    success_url = reverse_lazy(
        "factura_create"
    )

    def form_valid(self, form):
        """
        Se ejecuta cuando el formulario
        es válido.
        """

        messages.success(
            self.request,
            "✅ Factura registrada exitosamente."
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Se ejecuta cuando existen
        errores en el formulario.
        """

        messages.error(
            self.request,
            "❌ No fue posible registrar la factura. Revise los campos obligatorios."
        )

        return super().form_invalid(form)