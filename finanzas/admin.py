from django.contrib import admin
from .models import (
    Cliente,
    Proveedor,
    FacturaCompra
)

admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(FacturaCompra)