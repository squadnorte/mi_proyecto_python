from django.shortcuts import render, redirect, get_object_or_404
from .models import Parametro
from django.contrib.auth.decorators import login_required
from .forms import ParametroForm
from itsdangerous import URLSafeSerializer
from mi_proyecto.validators import validar_palabras_reservadas_y_caracteres
from django.core.exceptions import ValidationError
from django.conf import settings

# Configura el serializador con una clave secreta de settings.py
serializer = URLSafeSerializer(settings.ITS_DANGEROUS_SECRET_KEY)

# Funciones para generar y verificar IDs cifrados
def generar_id_cifrado(id):
    return serializer.dumps(id)

def verificar_id_cifrado(token):
    try:
        return serializer.loads(token)
    except:
        return None

# Vista para listar parámetros
@login_required
def listar_parametros(request):
    parametros = Parametro.objects.all()
    # Generar los IDs cifrados y construir un diccionario
    parametros_cifrados = [
        {
            'parametro': parametro,
            'id_cifrado': generar_id_cifrado(parametro.codigo_parametro)
        }
        for parametro in parametros
    ]
    return render(request, 'parametria/lista_parametros.html', {'parametros_cifrados': parametros_cifrados})

# Vista para crear un nuevo parámetro
@login_required
def crear_parametro(request):
    if request.method == 'POST':
        form = ParametroForm(request.POST)
        if form.is_valid():
            try:
                parametro = form.save(commit=False)
                parametro.usuario_auditoria = request.user

                # Validar palabras reservadas en los campos
                campos_a_validar = {
                    'nombre_parametro': parametro.nombre_parametro,
                    'valor_parametro': parametro.valor_parametro,
                    'abreviatura_parametro': parametro.abreviatura_parametro
                }

                # Realizar la validación para cada campo
                for campo, valor in campos_a_validar.items():
                    error_validacion = validar_palabras_reservadas_y_caracteres(valor)
                    if error_validacion:
                        form.add_error(campo, error_validacion)

                # Si hay errores, mostrar el formulario con los errores
                if form.errors:
                    return render(request, 'parametria/form_parametro.html', {'form': form})

                # Guardar el parámetro si no hay errores
                parametro.save()
                return redirect('config:list')

            except ValidationError as ve:
                # Manejar la ValidationError y agregarla al formulario
                form.add_error(None, str(ve))
                return render(request, 'parametria/form_parametro.html', {'form': form})

            except Exception as e:
                # Capturar cualquier otro error inesperado y redirigir a la página de error
                print(f"Error inesperado al crear parámetro: {e}")
                return render(request, 'error.html', {'mensaje': "Error inesperado al crear el parámetro. Por favor, inténtalo de nuevo."})
        else:
            print("Errores del formulario:", form.errors)
    else:
        form = ParametroForm()

    return render(request, 'parametria/form_parametro.html', {'form': form})

# Vista para editar un parámetro existente usando el token cifrado
@login_required
def editar_parametro(request, token):
    codigo_parametro = verificar_id_cifrado(token)
    if codigo_parametro is None:
        return render(request, 'error.html', {'mensaje': 'Token inválido o expirado'})

    parametro = get_object_or_404(Parametro, codigo_parametro=codigo_parametro)
    
    if request.method == 'POST':
        form = ParametroForm(request.POST, instance=parametro)
        if form.is_valid():
            try:
                # Validar palabras reservadas en los campos
                campos_a_validar = {
                    'nombre_parametro': form.cleaned_data.get('nombre_parametro'),
                    'valor_parametro': form.cleaned_data.get('valor_parametro'),
                    'abreviatura_parametro': form.cleaned_data.get('abreviatura_parametro')
                }

                # Realizar la validación para cada campo
                for campo, valor in campos_a_validar.items():
                    error_validacion = validar_palabras_reservadas_y_caracteres(valor)
                    if error_validacion:
                        form.add_error(campo, error_validacion)

                # Si hay errores, mostrar el formulario con los errores
                if form.errors:
                    return render(request, 'parametria/form_parametro.html', {'form': form})

                # Guardar el parámetro si no hay errores
                form.save()
                return redirect('config:list')

            except ValidationError as ve:
                # Manejar la ValidationError y agregarla al formulario
                form.add_error(None, str(ve))
                return render(request, 'parametria/form_parametro.html', {'form': form})

            except Exception as e:
                # Capturar cualquier otro error inesperado y redirigir a la página de error
                print(f"Error inesperado al editar parámetro: {e}")
                return render(request, 'error.html', {'mensaje': "Error inesperado al editar el parámetro. Por favor, inténtalo de nuevo."})
        else:
            print("Errores del formulario:", form.errors)
    else:
        form = ParametroForm(instance=parametro)

    return render(request, 'parametria/form_parametro.html', {'form': form})

# Vista para cambiar el estado de un parámetro usando el token cifrado
@login_required
def cambiar_estado_parametro(request, token):
    codigo_parametro = verificar_id_cifrado(token)
    if codigo_parametro is None:
        return render(request, 'error.html', {'mensaje': 'Token inválido o expirado'})  # Redirige a la página de error personalizada

    parametro = get_object_or_404(Parametro, codigo_parametro=codigo_parametro)
    if request.method == 'POST':
        parametro.estado_auditoria = 'inactivo'
        parametro.save()
        return redirect('config:list')

    return redirect('config:list')




