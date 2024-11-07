import os
import datetime
from dotenv import load_dotenv
from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

load_dotenv()

class SessionTimeoutMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        self.get_response = get_response

    def process_request(self, request):
        if request.user.is_authenticated:
            print("Usuario autenticado, verificando inactividad...")
            current_datetime = datetime.datetime.now()
            last_activity = request.session.get('last_activity')

            if last_activity:
                last_activity_time = datetime.datetime.strptime(last_activity, "%Y-%m-%d %H:%M:%S.%f")
                session_age = (current_datetime - last_activity_time).seconds
                print(f"Tiempo de inactividad: {session_age} segundos")

                # Obtiene el tiempo de inactividad personalizado desde las variables de entorno
                custom_timeout = int(os.getenv('SESSION_TIMEOUT', 1800))
                if session_age > custom_timeout:
                    print("Tiempo de inactividad excedido, cerrando sesión...")
                    auth.logout(request)
                    # Redirige al usuario a la página de login
                    return redirect('usuarios:login')  # Usa 'usuarios:login' para redirigir al login

            # Actualiza la última actividad
            request.session['last_activity'] = str(current_datetime)



