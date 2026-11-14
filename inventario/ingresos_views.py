import logging
import os
from decimal import Decimal, ROUND_HALF_UP
from uuid import uuid4

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import DataError, IntegrityError, connection, transaction
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from finanzas.models import FacturaCompra


logger = logging.getLogger(__name__)

UNIDADES = {
    "unidad": "Unidades",
    "m": "Metros (m)",
    "kg": "Kilogramos (kg)",
    "l": "Litros (L)",
}

ALIAS_UNIDADES = {
    "un": "unidad",
    "unidades": "unidad",
    "metro": "m",
    "metros": "m",
    "m2": "m²",
    "metros cuadrados": "m²",
    "m3": "m³",
    "metros cúbicos": "m³",
    "litro": "l",
    "litros": "l",
    "kilo": "kg",
    "kilos": "kg",
    "kilogramo": "kg",
    "kilogramos": "kg",
}


def tipo_movimiento_ingreso():
    return os.getenv("FYAG_TIPO_INGRESO", "").strip() or "INGRESO"


def consultar_articulos():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, codigo_parte, descripcion, unidad_medida
            FROM public.inventario_repuesto
            ORDER BY descripcion, codigo_parte, id
        """)
        return cursor.fetchall()


class FacturaField(forms.ModelChoiceField):
    def label_from_instance(self, factura):
        return (
            f"{factura.numero_documento} — {factura.proveedor.razon_social}"
            f" — {factura.fecha:%d/%m/%Y}"
        )


class IngresoForm(forms.Form):
    solicitud_id = forms.UUIDField(widget=forms.HiddenInput)

    factura = FacturaField(
        queryset=FacturaCompra.objects.none(),
        empty_label="Selecciona una factura",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    articulo = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    cantidad = forms.DecimalField(
        label="Cantidad recibida",
        max_digits=15,
        decimal_places=2,
        min_value=Decimal("0.01"),
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
    )

    unidad = forms.ChoiceField(
        label="Unidad de medida",
        choices=[("", "Selecciona una unidad"), *UNIDADES.items()],
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    precio = forms.DecimalField(
        label="Precio unitario neto (CLP)",
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.00"),
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
    )

    def __init__(self, articulos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["factura"].queryset = (
            FacturaCompra.objects.select_related("proveedor")
            .order_by("-fecha", "-pk")
        )
        self.fields["articulo"].choices = [
            ("", "Selecciona un artículo"),
            *((str(pk), f"{codigo} — {nombre} ({unidad})")
              for pk, codigo, nombre, unidad in articulos),
        ]

    def clean(self):
        datos = super().clean()
        cantidad = datos.get("cantidad")
        if datos.get("unidad") == "unidad" and cantidad is not None:
            if cantidad != cantidad.to_integral_value():
                self.add_error(
                    "cantidad",
                    "Los artículos por unidad requieren una cantidad entera.",
                )
        return datos


class IngresoRepetido(Exception):
    pass


@transaction.atomic
def guardar_ingreso(datos, responsable_id, tipo):
    cantidad = datos["cantidad"]
    precio = datos["precio"]
    subtotal = (cantidad * precio).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

    factura = (
        FacturaCompra.objects.select_for_update()
        .filter(pk=datos["factura"].pk)
        .first()
    )
    if factura is None:
        raise forms.ValidationError("La factura seleccionada ya no existe.")

    articulo_id = int(datos["articulo"])

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT unidad_medida
            FROM public.inventario_repuesto
            WHERE id = %s
            FOR UPDATE
        """, [articulo_id])
        articulo = cursor.fetchone()
        if articulo is None:
            raise forms.ValidationError("El artículo seleccionado ya no existe.")

        unidad_catalogo = articulo[0]
        clave = unidad_catalogo.strip().casefold()
        unidad_normalizada = ALIAS_UNIDADES.get(clave, clave)
        if datos["unidad"] != unidad_normalizada:
            raise forms.ValidationError(
                f"Selecciona la unidad del catálogo: {unidad_catalogo}."
            )

        cursor.execute("""
            INSERT INTO public.inventario_movimientobodega
                (tipo, cantidad, fecha_registro, numero_ot, repuesto_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, [tipo, cantidad, timezone.now(), "", articulo_id])
        movimiento_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO public.recepciones_ingreso
                (solicitud_id, factura_id, movimiento_id, responsable_id,
                 unidad_medida, precio_unitario_neto, subtotal_neto)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (solicitud_id) DO NOTHING
            RETURNING solicitud_id
        """, [
            datos["solicitud_id"], factura.pk, movimiento_id, responsable_id,
            datos["unidad"], precio, subtotal,
        ])
        if cursor.fetchone() is None:
            raise IngresoRepetido

        cursor.execute("""
            UPDATE public.inventario_repuesto
            SET stock_actual = stock_actual + %s
            WHERE id = %s
        """, [cantidad, articulo_id])


@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def registrar_ingreso(request):
    if request.user.rol != "bodega":
        raise PermissionDenied

    articulos = consultar_articulos()
    unidades_articulos = {}
    for pk, _, _, unidad in articulos:
        clave = unidad.strip().casefold()
        unidades_articulos[str(pk)] = ALIAS_UNIDADES.get(clave, clave)

    with connection.cursor() as cursor:
        cursor.execute("SELECT to_regclass('public.recepciones_ingreso') IS NOT NULL")
        guardado_disponible = cursor.fetchone()[0]

    form = IngresoForm(
        articulos,
        request.POST if request.method == "POST" else None,
        initial={"solicitud_id": uuid4()},
    )

    if guardado_disponible and request.method == "POST" and form.is_valid():
        tipo = tipo_movimiento_ingreso()
        tipo_salida = os.getenv("FYAG_TIPO_SALIDA", "").strip()
        if len(tipo) > 10 or tipo.casefold() == tipo_salida.casefold():
            form.add_error(None, "Revisa la configuración de los tipos de movimiento.")
        else:
            try:
                guardar_ingreso(form.cleaned_data, request.user.pk, tipo)
            except IngresoRepetido:
                messages.info(request, "Este formulario ya se había enviado.")
                return redirect("inventario:ingresos")
            except forms.ValidationError as error:
                form.add_error(None, error)
            except (DataError, IntegrityError):
                logger.exception("Error al guardar un ingreso de bodega")
                form.add_error(None, "No se pudo guardar el ingreso. Revisa los datos y el stock.")
            else:
                messages.success(request, "Ingreso registrado y stock actualizado.")
                return redirect("inventario:ingresos")

    return render(request, "registrar_ingreso.html", {
        "form": form,
        "unidades_articulos": unidades_articulos,
        "guardado_disponible": guardado_disponible,
    })