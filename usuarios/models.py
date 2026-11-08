from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class Trabajador(AbstractUser):
    rut = models.CharField(
        max_length=10,
        blank=False,
        null=True,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^\d{8}-[\dK]$',
                message='Ingrese el RUT con el formato 12345678-9 (use K si corresponde).',
            )
        ],
        error_messages={'unique': 'Ya existe un usuario con este RUT.'},
    )
    telefono = models.CharField(max_length=15, blank=True, null=True)

    @property
    def rol(self):
        if self.groups.filter(name__iexact='Gerencia').exists():
            return 'gerencia'
        if self.groups.exists():
            return self.groups.first().name.lower()
        return ''

    def __str__(self):
        return f"{self.username} - {self.get_full_name()}"