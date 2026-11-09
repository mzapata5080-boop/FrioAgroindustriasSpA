from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Trabajador
from .forms import TrabajadorCrearForm, TrabajadorEditarForm

# ==========================================

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        usuario = request.POST.get('username')
        contrasena = request.POST.get('password')
        
        user = authenticate(request, username=usuario, password=contrasena)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales incorrectas. Verifique su usuario y contraseña.')
            
    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def custom_logout(request):
    logout(request)
    return redirect('login')

class TrabajadorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Trabajador
    form_class = TrabajadorCrearForm
    template_name = 'usuarios/trabajador_form.html'
    success_url = reverse_lazy('trabajador_list')

    raise_exception = True

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.rol == 'gerencia'

    def form_valid(self, form):
        messages.success(self.request, '¡Trabajador creado exitosamente!')
        return super().form_valid(form)


class TrabajadorUpdateView(LoginRequiredMixin, UpdateView):
    model = Trabajador
    form_class = TrabajadorEditarForm
    template_name = 'usuarios/trabajador_form.html'
    success_url = reverse_lazy('trabajador_list')

    def form_valid(self, form):
        messages.success(self.request, '¡Trabajador actualizado exitosamente!')
        return super().form_valid(form)


class TrabajadorDeleteView(LoginRequiredMixin, DeleteView):
    model = Trabajador
    template_name = 'usuarios/trabajador_confirm_delete.html'
    success_url = reverse_lazy('trabajador_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'El trabajador ha sido eliminado correctamente.')
        return super().delete(request, *args, **kwargs)
    
class TrabajadorListView(LoginRequiredMixin, ListView):
    model = Trabajador
    template_name = 'usuarios/trabajador_list.html'
    context_object_name = 'trabajadores'