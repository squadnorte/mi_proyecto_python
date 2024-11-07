from django.urls import path
from . import views
from .views import crear_tarea_jira, desasignar_habilitador
from django.views.generic import RedirectView

app_name = 'habin'

urlpatterns = [
    path('list/', views.listar_iniciativas, name='list'),
    path('new/', views.crear_iniciativa, name='new'),  # Asegúrate de que esté definido con este name
    path('edit/<str:token>/', views.editar_iniciativa, name='edit'),  # Editar cabecera y habilitadores usando token cifrado
    path('generar_reporte/', views.generar_reporte_iniciativas, name='generar_reporte_iniciativas'),
    path('exportar_excel/', views.exportar_reporte_excel, name='exportar_reporte_excel'),
    path('crear_tarea_jira/<str:token>/<int:habilitador_codigo>/', views.crear_tarea_jira, name='crear_tarea_jira'),
    path('delete/<str:token>/', desasignar_habilitador, name='delete'),  # Usar token cifrado
    path('', RedirectView.as_view(url='/admin/', permanent=False)),  # Redirige la raíz a la admin
]






