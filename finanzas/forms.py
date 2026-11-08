from django import forms
from .models import Cliente


class ClienteForm(forms.ModelForm):
    """
    Formulario para crear y editar clientes.
    """

    class Meta:
        model = Cliente
        fields = "__all__"

        fields = [
            "rut",
            "razon_social",
            "telefono",
            "correo",
            "direccion"
        ]

    def clean_rut(self):
        """
        Evita registrar clientes duplicados.
        """

        rut = self.cleaned_data["rut"]

        if Cliente.objects.filter(rut=rut).exists():
            raise forms.ValidationError(
                "Este RUT ya existe."
            )

        return rut

widgets = {

    'rut': forms.TextInput(
        attrs={
            'class':'form-control'
        }
    ),

    'razon_social': forms.TextInput(
        attrs={
            'class':'form-control'
        }
    ),

    'telefono': forms.TextInput(
        attrs={
            'class':'form-control'
        }
    ),

    'correo': forms.EmailInput(
        attrs={
            'class':'form-control'
        }
    ),

    'direccion': forms.TextInput(
        attrs={
            'class':'form-control'
        }
    ),
}