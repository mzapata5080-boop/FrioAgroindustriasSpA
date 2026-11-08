from django.db import models


class Cliente(models.Model):
    """
    Representa los clientes de Frío y Agroindustria.

    Un cliente puede tener una o varias obras
    asociadas dentro del sistema.
    """

    rut = models.CharField(
        max_length=12,
        unique=True
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

    def __str__(self):
        """
        Retorna el nombre del cliente
        cuando se visualice en Django Admin.
        """
        return self.razon_social