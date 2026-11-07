from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['rut', 'razon_social', 'giro', 'telefono', 'email', 'direccion']
        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '12345678-9'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Razón Social o Empresa'}),
            'giro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Giro del Negocio'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+56 9 1234 5678'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contacto@empresa.cl'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut', '')
        rut_limpio = rut.upper().replace(".", "").replace("-", "")
        if len(rut_limpio) > 1:
            return f"{rut_limpio[:-1]}-{rut_limpio[-1]}"
        return rut