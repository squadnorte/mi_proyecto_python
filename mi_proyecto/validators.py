import re
from django.core.exceptions import ValidationError

# Lista de palabras reservadas que quieres evitar
PALABRAS_RESERVADAS = [
    'DROP', 'DELETE', 'UPDATE', 'INSERT', 'SELECT', 'ALTER', 'TABLE', 'TRUNCATE'
]

# Expresión regular para caracteres especiales no deseados
CARACTERES_ESPECIALES = re.compile(r'[<>;{}$]')

def validar_palabras_reservadas_y_caracteres(value):
    # Asegurarse de que el valor es una cadena
    if not isinstance(value, str):
        value = str(value)  # Convertir a cadena si no lo es

    # Verificar si contiene palabras reservadas
    for palabra in PALABRAS_RESERVADAS:
        if palabra in value.upper():  # Comparar sin distinguir mayúsculas/minúsculas
            raise ValidationError(f'El texto contiene la palabra reservada "{palabra}".')

    # Verificar si contiene caracteres especiales no permitidos
    if CARACTERES_ESPECIALES.search(value):
        raise ValidationError('El texto contiene caracteres especiales no permitidos.')

