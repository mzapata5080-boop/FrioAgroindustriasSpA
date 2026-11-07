import re
from django.core.exceptions import ValidationError

def validar_rut_chileno(value):
    # Limpiar puntos, espacios y guiones, convertir a mayúsculas
    rut = str(value).upper().replace(".", "").replace("-", "").strip()
    
    # Validar formato de largo (7 u 8 dígitos + cuerpo k/K o número)
    if not re.match(r"^\d{7,8}[0-9K]$", rut):
        raise ValidationError("El RUT no tiene un formato válido (ej: 76132049-4).")
    
    cuerpo = rut[:-1]
    dv_ingresado = rut[-1]
    
    # Algoritmo Módulo 11 exacto
    suma = 0
    multiplicador = 2
    
    for digit in reversed(cuerpo):
        suma += int(digit) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1
        
    resto = suma % 11
    resultado = 11 - resto
    
    if resultado == 11:
        dv_esperado = "0"
    elif resultado == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(resultado)
        
    if str(dv_ingresado) != str(dv_esperado):
        raise ValidationError("El RUT ingresado no es válido.")