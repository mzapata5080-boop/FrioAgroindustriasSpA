from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from .models import Trabajador

ROLES_CHOICES = [
    ('', 'Seleccione un rol...'),
    ('Gerencia', 'Gerencia'),
    ('Finanzas', 'Finanzas'),
    ('Bodega', 'Bodega'),
    ('Supervisor de Obra', 'Supervisor de Obra'),
]

class TrabajadorCrearForm(UserCreationForm):
    rol = forms.ChoiceField(
        choices=ROLES_CHOICES,
        required=True,
        label='Rol en la empresa',
        widget=forms.Select(attrs={'class': 'form-select', 'required': 'required'})
    )

    class Meta(UserCreationForm.Meta):
        model = Trabajador
        fields = ('username', 'first_name', 'last_name', 'email', 'rut', 'telefono', 'rol')
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'rut': 'RUT',
            'telefono': 'Teléfono',
            'rol': 'Rol / Cargo',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_email', 'autocomplete': 'off'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password1' in self.fields:
            self.fields['password1'].label = "Contraseña"
        if 'password2' in self.fields:
            self.fields['password2'].label = "Confirmación de contraseña"

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            rol_nombre = self.cleaned_data.get('rol')
            if rol_nombre:
                grupo, _ = Group.objects.get_or_create(name=rol_nombre)
                user.groups.add(grupo)
        return user


class TrabajadorEditarForm(UserChangeForm):
    password = None
    rol = forms.ChoiceField(
        choices=ROLES_CHOICES,
        required=True,
        label='Rol en la empresa',
        widget=forms.Select(attrs={'class': 'form-select', 'required': 'required'})
    )

    class Meta:
        model = Trabajador
        fields = ('username', 'first_name', 'last_name', 'email', 'rut', 'telefono', 'is_active', 'rol')
        labels = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'rut': 'RUT',
            'telefono': 'Teléfono',
            'is_active': 'Estado Activo',
            'rol': 'Rol / Cargo',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_email'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.groups.exists():
            self.fields['rol'].initial = self.instance.groups.first().name

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.groups.clear()
            rol_nombre = self.cleaned_data.get('rol')
            if rol_nombre:
                grupo, _ = Group.objects.get_or_create(name=rol_nombre)
                user.groups.add(grupo)
        return user