from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError, connection, transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .ingresos_views import UNIDADES


class ArticuloForm(forms.Form):
    codigo = forms.CharField(label="Código de parte", max_length=50)
    descripcion = forms.CharField(label="Nombre o descripción", max_length=200)
    ubicacion = forms.CharField(label="Ubicación en bodega", max_length=50)
    categoria = forms.ChoiceField(label="Categoría existente", required=False)
    categoria_nueva = forms.CharField(
        label="Nueva categoría", max_length=100, required=False
    )
    unidad = forms.ChoiceField(
        label="Unidad de medida",
        choices=[("", "Selecciona una unidad"), *UNIDADES.items()],
    )

    def __init__(self, categorias, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["categoria"].choices = [
            ("", "Selecciona una categoría"),
            *((str(pk), nombre) for pk, nombre in categorias),
        ]
        for campo in self.fields.values():
            campo.widget.attrs["class"] = (
                "form-select" if isinstance(campo.widget, forms.Select)
                else "form-control"
            )

    def clean(self):
        datos = super().clean()
        if "categoria" in datos and "categoria_nueva" in datos:
            if bool(datos["categoria"]) == bool(datos["categoria_nueva"]):
                raise ValidationError(
                    "Selecciona una categoría existente o escribe una nueva."
                )
        return datos


@transaction.atomic
def guardar_articulo(datos):
    with connection.cursor() as cursor:
        if datos["categoria_nueva"]:
            nombre = datos["categoria_nueva"]

            # Evita crear la misma categoría en dos altas simultáneas.
            cursor.execute("""
                LOCK TABLE public.inventario_categoriarepuesto
                IN SHARE ROW EXCLUSIVE MODE
            """)
            cursor.execute("""
                SELECT id
                FROM public.inventario_categoriarepuesto
                WHERE lower(btrim(nombre)) = lower(%s)
                ORDER BY id
                LIMIT 1
            """, [nombre])
            categoria = cursor.fetchone()

            if categoria is None:
                cursor.execute("""
                    INSERT INTO public.inventario_categoriarepuesto (nombre)
                    VALUES (%s)
                    RETURNING id
                """, [nombre])
                categoria = cursor.fetchone()
        else:
            cursor.execute("""
                SELECT id
                FROM public.inventario_categoriarepuesto
                WHERE id = %s
                FOR KEY SHARE
            """, [int(datos["categoria"])])
            categoria = cursor.fetchone()

            if categoria is None:
                raise ValidationError("La categoría seleccionada ya no existe.")

        cursor.execute("""
            INSERT INTO public.inventario_repuesto (
                codigo_parte, descripcion, ubicacion_bodega,
                unidad_medida, stock_actual, stock_minimo, categoria_id
            )
            VALUES (%s, %s, %s, %s, 0, 0, %s)
            ON CONFLICT (codigo_parte) DO NOTHING
            RETURNING id
        """, [
            datos["codigo"],
            datos["descripcion"],
            datos["ubicacion"],
            datos["unidad"],
            categoria[0],
        ])

        if cursor.fetchone() is None:
            raise ValidationError({"codigo": "Ya existe un artículo con ese código."})


@login_required(login_url="login")
@require_http_methods(["GET", "POST"])
def crear_articulo(request):
    if request.user.rol != "bodega":
        raise PermissionDenied

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, nombre
            FROM public.inventario_categoriarepuesto
            ORDER BY nombre, id
        """)
        categorias = cursor.fetchall()

    form = ArticuloForm(
        categorias,
        request.POST if request.method == "POST" else None,
    )

    if request.method == "POST" and form.is_valid():
        try:
            guardar_articulo(form.cleaned_data)
        except ValidationError as error:
            form.add_error(None, error)
        except IntegrityError:
            form.add_error(None, "No se pudo guardar el artículo. Revisa los datos.")
        else:
            messages.success(request, "Artículo creado con stock inicial de 0.")
            return redirect("inventario:stock")

    return render(request, "crear_articulo.html", {
        "form": form,
        "hay_categorias": bool(categorias),
    })