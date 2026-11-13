import os

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render
from django.utils import timezone


@login_required(login_url="login")
def stock(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT codigo_parte, descripcion, ubicacion_bodega,
                   unidad_medida, stock_actual, stock_minimo
            FROM public.inventario_repuesto
            ORDER BY descripcion, codigo_parte
        """)
        repuestos = cursor.fetchall()

    registros = [
        {
            "material": descripcion,
            "critico": actual <= minimo,
            "campos": [
                ("Código", codigo),
                ("Ubicación", ubicacion),
                ("Stock disponible", f"{actual} {unidad}"),
                ("Stock mínimo", f"{minimo} {unidad}"),
            ],
        }
        for codigo, descripcion, ubicacion, unidad, actual, minimo in repuestos
    ]

    return render(request, "listado.html", {
        "titulo": "Inventario",
        "seccion": "stock",
        "registros": registros,
    })


@login_required(login_url="login")
def movimientos(request, seccion):
    titulo = "Ingresos de bodega" if seccion == "ingresos" else "Salidas de bodega"
    tipo_ingreso = os.getenv("FYAG_TIPO_INGRESO", "").strip()
    tipo_salida = os.getenv("FYAG_TIPO_SALIDA", "").strip()
    contexto = {"titulo": titulo, "seccion": seccion}

    if not tipo_ingreso or not tipo_salida or tipo_ingreso == tipo_salida:
        contexto["aviso"] = "Falta configurar los tipos de ingreso y salida."
        return render(request, "listado.html", contexto)

    tipo = tipo_ingreso if seccion == "ingresos" else tipo_salida
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT r.descripcion, r.unidad_medida, m.cantidad,
                   m.fecha_registro, m.numero_ot
            FROM public.inventario_movimientobodega AS m
            JOIN public.inventario_repuesto AS r ON r.id = m.repuesto_id
            WHERE m.tipo = %s
            ORDER BY m.fecha_registro DESC, m.id DESC
        """, [tipo])
        filas = cursor.fetchall()

    contexto["registros"] = [
        {
            "material": descripcion,
            "campos": [
                ("Fecha", timezone.template_localtime(fecha).strftime("%d/%m/%Y %H:%M")),
                ("Cantidad", f"{cantidad} {unidad}"),
                ("Orden de trabajo", numero_ot or "Sin orden asociada"),
            ],
        }
        for descripcion, unidad, cantidad, fecha, numero_ot in filas
    ]
    return render(request, "listado.html", contexto)