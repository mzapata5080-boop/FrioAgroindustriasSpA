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


class RutField(forms.RegexField):
    def __init__(self, **kwargs):
        super().__init__(
            regex=r'^\d{8}-[\dK]$',
            max_length=10,
            label='RUT',
            help_text='Formato: 12345678-9 (use K como dígito verificador cuando corresponda).',
            error_messages={
                'invalid': 'Ingrese el RUT con el formato 12345678-9 (use K si corresponde).',
            },
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345678-9',
                'maxlength': '10',
                'pattern': '[0-9]{8}-[0-9K]',
                'title': 'Formato: 12345678-9 (use K si corresponde).',
            }),
            **kwargs,
        )


class TrabajadorCrearForm(UserCreationForm):
    rut = RutField()
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
            'telefono': 'Teléfono',
            'rol': 'Rol / Cargo',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_email', 'autocomplete': 'off'}),
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
    rut = RutField()
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
            'telefono': 'Teléfono',
            'is_active': 'Estado Activo',
            'rol': 'Rol / Cargo',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_email'}),
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