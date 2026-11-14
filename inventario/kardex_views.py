import os

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import connection
from django.shortcuts import render
from django.views.decorators.http import require_safe


@login_required(login_url="login")
@require_safe
def kardex(request):
    if not (request.user.is_superuser or request.user.rol == "gerencia"):
        raise PermissionDenied

    colores = {
        "ingreso": "success",
        "salida": "salida",
        "merma": "danger",
        "ajuste": "ajuste",
        "reversa": "ajuste",
    }
    for variable, color in (
        ("FYAG_TIPO_INGRESO", "success"),
        ("FYAG_TIPO_SALIDA", "salida"),
    ):
        tipo_configurado = os.getenv(variable, "").strip().casefold()
        if tipo_configurado:
            colores[tipo_configurado] = color

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT m.fecha_registro, r.descripcion, m.tipo,
                   m.cantidad, r.unidad_medida, m.numero_ot
            FROM public.inventario_movimientobodega AS m
            JOIN public.inventario_repuesto AS r ON r.id = m.repuesto_id
            ORDER BY m.fecha_registro DESC, m.id DESC
        """)
        filas = cursor.fetchall()

    movimientos = [
        {
            "fecha": fecha,
            "articulo": articulo,
            "tipo": tipo,
            "color": colores.get(tipo.strip().casefold(), "secondary"),
            "cantidad": cantidad,
            "unidad": unidad,
            "numero_ot": numero_ot,
        }
        for fecha, articulo, tipo, cantidad, unidad, numero_ot in filas
    ]

    return render(request, "kardex.html", {"movimientos": movimientos})