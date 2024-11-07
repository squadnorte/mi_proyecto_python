from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from itsdangerous import URLSafeSerializer
from django.conf import settings
from axes.helpers import get_lockout_response
from mi_proyecto.validators import validar_palabras_reservadas_y_caracteres
from django.core.exceptions import ValidationError
from django.contrib.auth import logout

from .forms import LoginForm, RegistroForm

# Configuración para el cifrado
serializer = URLSafeSerializer(settings.ITS_DANGEROUS_SECRET_KEY)

# Función para generar el ID cifrado
def generar_id_cifrado(id):
    return serializer.dumps(id)

# Función para verificar el ID cifrado
def verificar_id_cifrado(token):
    try:
        return serializer.loads(token)
    except:
        return None

def home_view(request):
    return render(request, 'usuarios/home.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('user:home')  # Redirigir a la página de inicio
            else:
                form.add_error(None, 'Nombre de usuario o contraseña incorrectos')
                
                # Verificar si la cuenta está bloqueada y mostrar el mensaje
                lockout_response = get_lockout_response(request)
                if lockout_response:
                    messages.error(request, "Cuenta bloqueada: demasiados intentos de inicio de sesión. Inténtelo de nuevo más tarde.")
                    return lockout_response
    else:
        form = LoginForm()

    return render(request, 'usuarios/login.html', {'form': form})
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)  # Encripta la contraseña
            user.save()
            login(request, user)  # Inicia sesión automáticamente después del registro
            return redirect('user:home')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})

@login_required
def gestion_usuarios_view(request):
    query = request.GET.get('q')
    if query:
        usuarios = User.objects.filter(username__icontains=query) | User.objects.filter(email__icontains=query)
    else:
        usuarios = User.objects.all()
    
    context = {
        'usuarios': usuarios,
        'query': query
    }
    return render(request, 'usuarios/gestion_usuarios.html', context)

@login_required
def registro_usuario_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if 'guardar' in request.POST:
            if form.is_valid():
                # Validar campos específicos
                campos_a_validar = {
                    'username': form.cleaned_data.get('username'),
                    'email': form.cleaned_data.get('email'),
                    'first_name': form.cleaned_data.get('first_name'),
                    'last_name': form.cleaned_data.get('last_name'),
                }

                # Aplicar validaciones y agregar errores al formulario si los hay
                for campo, valor in campos_a_validar.items():
                    try:
                        validar_palabras_reservadas_y_caracteres(valor)
                    except ValidationError as ve:
                        form.add_error(campo, str(ve))

                if not form.errors:  # Verifica que no haya errores después de las validaciones
                    user = form.save(commit=False)
                    password = form.cleaned_data['password']
                    user.set_password(password)
                    user.save()
                    return redirect('user:gestion_usuarios')

        elif 'cancelar' in request.POST:
            return redirect('user:gestion_usuarios')

    else:
        form = RegistroForm()

    context = {'form': form}
    return render(request, 'usuarios/registro_usuario.html', context)
def logout_view(request):
    logout(request)
    return redirect('user:login')  # Redirige al usuario a la página de inicio de sesión

