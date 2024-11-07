from django.urls import path
from . import views

app_name = 'hab'

urlpatterns = [
    path('list/', views.listar_habilitadores, name='list'),
    path('new/', views.crear_habilitador, name='new'),
    path('edit/<str:token>/', views.editar_habilitador, name='edit'),  # Cambiado a token
    path('delete/<str:token>/', views.cambiar_estado_habilitador, name='delete'),  # Cambiado a token
]





