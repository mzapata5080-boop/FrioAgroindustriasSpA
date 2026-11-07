from django.db import models
from .validators import validar_rut_chileno

class Proveedor(models.Model):
    rut = models.CharField(max_length=12, unique=True, validators=[validar_rut_chileno], verbose_name="RUT")
    razon_social = models.CharField(max_length=150, verbose_name="Razón Social / Nombre")
    giro = models.CharField(max_length=100, verbose_name="Giro")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Correo Electrónico")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    creado_el = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return f"{self.rut} - {self.razon_social}"  