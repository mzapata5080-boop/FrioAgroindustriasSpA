from django.db import models
from django.contrib.auth.models import AbstractUser

class Trabajador(AbstractUser):
    ROLES = (
        ('gerencia', 'Administración y Gerencia'),
        ('finanzas', 'Administrativo y Finanzas'),
        ('bodega', 'Bodega'),
        ('obras', 'Supervisor de Obras'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='bodega')

    def __str__(self):
        return f"{self.username} - {self.rol}"