from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Proveedor
from .forms import ProveedorForm

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