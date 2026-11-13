from django import forms
from .models import Cliente, Proveedor
from .models import (Cliente,Proveedor,FacturaCompra)

class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente

        fields = [
            'rut',
            'razon_social',
            'telefono',
            'correo',
            'direccion'
        ]

        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')

        if Cliente.objects.filter(rut=rut)\
                .exclude(pk=self.instance.pk)\
                .exists():

            raise forms.ValidationError(
                "Ya existe un cliente con este RUT."
            )

        return rut


class Meta:
        model = Cliente
        fields = [
            'rut',
            'razon_social',
            'telefono',
            'correo',
            'direccion'
        ]

        widgets = {
            'rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345678-9'
            }),

            'razon_social': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Razón Social'
            }),

            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 9 1234 5678'
            }),

            'correo': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@empresa.cl'
            }),

            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección'
            }),
        }

class ProveedorForm(forms.ModelForm):

    class Meta:
        model = Proveedor

        fields = [
            'rut',
            'razon_social',
            'giro',
            'telefono',
            'email',
            'direccion',
            'banco',
            'tipo_cuenta',
            'numero_cuenta'
        ]

        widgets = {
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'razon_social': forms.TextInput(attrs={'class': 'form-control'}),
            'giro': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'banco': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_cuenta': forms.Select(attrs={'class': 'form-control'}),
            'numero_cuenta': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut', '')

        rut_limpio = rut.upper().replace(".", "").replace("-", "")

        if len(rut_limpio) > 1:
            rut = f"{rut_limpio[:-1]}-{rut_limpio[-1]}"

        qs = Proveedor.objects.filter(rut=rut)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "Ya existe un cliente con este RUT."
            )

        return rut

class FacturaCompraForm(forms.ModelForm):

    class Meta:

        model = FacturaCompra

        fields = [
            'proveedor',
            'fecha',
            'numero_documento',
            'tipo_documento',
            'monto'
        ]

        widgets = {

            'fecha': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'proveedor': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'numero_documento': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'tipo_documento': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'monto': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }