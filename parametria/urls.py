from django.urls import path
from . import views

app_name = 'config'  # Un nombre genérico para el namespace

urlpatterns = [
    path('list/', views.listar_parametros, name='list'),  # Cambiado a 'list/'
    path('new/', views.crear_parametro, name='new'),  # Cambiado a 'new/'
    path('edit/<str:token>/', views.editar_parametro, name='edit'),  # Cambiado a 'edit/'
    path('delete/<str:token>/', views.cambiar_estado_parametro, name='delete'),  # Cambiado a 'delete/'
]






