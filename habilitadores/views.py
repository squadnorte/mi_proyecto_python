from django.shortcuts import render, redirect, get_object_or_404
from .models import HabilitadorCiberseguridad
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .forms import HabilitadorCiberseguridadForm
from parametria.models import Parametro
from django.core.paginator import Paginator
from django.db.models import Q
from itsdangerous import URLSafeSerializer
from mi_proyecto.validators import validar_palabras_reservadas_y_caracteres
from django.conf import settings
from django.utils import timezone

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

# Vista para listar habilitadores
@login_required
def listar_habilitadores(request):
    query = request.GET.get('q', '')
    habilitadores = HabilitadorCiberseguridad.objects.filter(estado_auditoria__valor_parametro='activo').select_related('imprescindible')

    # Aplicar búsqueda
    if query:
        habilitadores = habilitadores.filter(
            Q(codigo__icontains=query) |
            Q(dimension__valor_parametro__icontains=query) |
            Q(dominio__valor_parametro__icontains=query) |
            Q(titulo__icontains=query) |
            Q(imprescindible__valor_parametro__icontains=query)
        )

    # Paginación
    paginator = Paginator(habilitadores, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Generar IDs cifrados
    parametros_cifrados = [
        {
            'habilitador': habilitador,
            'id_cifrado': generar_id_cifrado(habilitador.pk)
        }
        for habilitador in page_obj
    ]

    return render(request, 'habilitadores/listar_habilitadores.html', {
        'page_obj': page_obj,
        'query': query,
        'parametros_cifrados': parametros_cifrados
    })

# Vista para crear un nuevo habilitador
from django.core.exceptions import ValidationError

@login_required
def crear_habilitador(request):
    if request.method == 'POST':
        form = HabilitadorCiberseguridadForm(request.POST)
        if form.is_valid():
            try:
                habilitador = form.save(commit=False)
                habilitador.usuario_auditoria = request.user.username
                habilitador.fecha_auditoria = datetime.now()

                # Validar palabras reservadas en todos los campos
                campos_a_validar = {
                    'titulo': habilitador.titulo,
                    'descripcion': habilitador.descripcion,
                    'observacion': habilitador.observacion,
                    'dimension': habilitador.dimension,
                    'dominio': habilitador.dominio,
                    'lineamiento': habilitador.lineamiento,
                    'imprescindible': habilitador.imprescindible,
                }

                # Realizar la validación para cada campo
                for campo, valor in campos_a_validar.items():
                    if valor:  # Asegúrate de que el valor no sea None
                        error_validacion = validar_palabras_reservadas_y_caracteres(valor)
                        if error_validacion:
                            form.add_error(campo, error_validacion)

                # Si hay errores, mostrar el formulario con los errores
                if form.errors:
                    return render(request, 'habilitadores/crear_habilitador.html', {'form': form})

                # Buscar el estado 'ACTIVO' en la tabla Parametro
                try:
                    estado_activo = Parametro.objects.get(nombre_parametro='ESTADO', valor_parametro='activo')
                    habilitador.estado_auditoria = estado_activo
                except Parametro.DoesNotExist:
                    form.add_error(None, "Error: No se encontró el estado 'ACTIVO' en la tabla Parametro.")
                    return render(request, 'habilitadores/crear_habilitador.html', {'form': form})

                habilitador.save()
                return redirect('hab:list')

            except ValidationError as ve:
                # Manejar la ValidationError y agregarla al formulario
                form.add_error(None, str(ve))
                return render(request, 'habilitadores/crear_habilitador.html', {'form': form})

            except Exception as e:
                # Capturar cualquier otro error inesperado y redirigir a la página de error
                print(f"Error inesperado al crear habilitador: {e}")
                return render(request, 'error.html', {'mensaje': "Error inesperado al crear el habilitador. Por favor, inténtalo de nuevo."})
        else:
            print("Errores del formulario:", form.errors)
    else:
        form = HabilitadorCiberseguridadForm()

    return render(request, 'habilitadores/crear_habilitador.html', {'form': form})

# Vista para editar un habilitador usando el token cifrado
@login_required
def editar_habilitador(request, token):
    # Verificar el ID descifrado a partir del token
    pk = verificar_id_cifrado(token)
    if pk is None:
        return render(request, 'error.html', {'mensaje': 'Token inválido o expirado'})

    # Obtener el habilitador correspondiente o devolver un error 404
    habilitador = get_object_or_404(HabilitadorCiberseguridad, pk=pk)
    
    if request.method == 'POST':
        form = HabilitadorCiberseguridadForm(request.POST, instance=habilitador)
        if form.is_valid():
            try:
                habilitador = form.save(commit=False)

                # Validar palabras reservadas en todos los campos
                campos_a_validar = {
                    'titulo': habilitador.titulo,
                    'descripcion': habilitador.descripcion,
                    'observacion': habilitador.observacion,
                    'dimension': habilitador.dimension,
                    'dominio': habilitador.dominio,
                    'lineamiento': habilitador.lineamiento,
                    'imprescindible': habilitador.imprescindible,
                }

                # Realizar la validación para cada campo
                for campo, valor in campos_a_validar.items():
                    error_validacion = validar_palabras_reservadas_y_caracteres(valor)
                    if error_validacion:
                        form.add_error(campo, error_validacion)

                # Si hay errores, mostrar el formulario con los errores
                if form.errors:
                    return render(request, 'habilitadores/editar_habilitador.html', {'form': form})

                # Guardar los cambios si todo es válido
                habilitador.save()
                return redirect('hab:list')

            except ValidationError as ve:
                # Manejar la ValidationError y agregarla al formulario
                form.add_error(None, str(ve))
                return render(request, 'habilitadores/editar_habilitador.html', {'form': form})

            except Exception as e:
                # Capturar cualquier otro error inesperado y redirigir a la página de error
                print(f"Error inesperado al editar habilitador: {e}")
                return render(request, 'error.html', {'mensaje': "Error inesperado al editar el habilitador. Por favor, inténtalo de nuevo."})
        else:
            print("Errores del formulario:", form.errors)
    else:
        form = HabilitadorCiberseguridadForm(instance=habilitador)
    
    return render(request, 'habilitadores/editar_habilitador.html', {'form': form})


# Vista para cambiar el estado de un habilitador usando el token cifrado
@login_required
def cambiar_estado_habilitador(request, token):
    pk = verificar_id_cifrado(token)
    if pk is None:
        return render(request, 'error.html', {'mensaje': 'Token inválido o expirado'})

    habilitador = get_object_or_404(HabilitadorCiberseguridad, pk=pk)
    
    # Buscar la instancia de 'inactivo' en la tabla Parametro
    try:
        estado_inactivo = Parametro.objects.get(nombre_parametro='ESTADO', valor_parametro='INACTIVO')
        habilitador.estado_auditoria = estado_inactivo
    except Parametro.DoesNotExist:
        return render(request, 'error.html', {'mensaje': "Error: No se encontró el estado 'INACTIVO' en la tabla Parametro."})

    habilitador.save()
    return redirect('hab:list')


