from django.db import models
from .validators import validar_rut_chileno


class Cliente(models.Model):

    rut = models.CharField(
        max_length=12,
        unique=True,
        validators=[validar_rut_chileno]
    )

    razon_social = models.CharField(
        max_length=150
    )

    telefono = models.CharField(
        max_length=20
    )

    correo = models.EmailField()

    direccion = models.CharField(
        max_length=200
    )

    creado_el = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.rut} - {self.razon_social}"


class Proveedor(models.Model):

    rut = models.CharField(
        max_length=12,
        unique=True,
        validators=[validar_rut_chileno]
    )

    razon_social = models.CharField(
        max_length=150
    )

    giro = models.CharField(
        max_length=100
    )

    telefono = models.CharField(
        max_length=20
    )

    email = models.EmailField()

    direccion = models.CharField(
        max_length=200
    )

    creado_el = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return f"{self.rut} - {self.razon_social}"