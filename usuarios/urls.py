from django.urls import path
from usuarios.views import home_view, gestion_usuarios_view, registro_usuario_view, login_view,logout_view

app_name = "user"

urlpatterns = [
    path('home/', home_view, name='home'),
    path('gestion-usuarios/', gestion_usuarios_view, name='gestion_usuarios'),
    path('nuevo-usuario/', registro_usuario_view, name='registro_usuario'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),  # Añade esta línea
]





