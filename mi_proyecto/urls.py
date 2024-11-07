from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from usuarios.views import home_view  # Importar la vista de inicio
from django.views.generic import RedirectView

urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('user/', include(('usuarios.urls', 'user'), namespace='user')),
    path('config/', include(('parametria.urls', 'config'),namespace='config')),  # Incluye el namespace aquí
   path('hab/', include('habilitadores.urls', namespace='hab')),
   path('habin/', include('habilitadores_iniciativa.urls', namespace='habin')),
    path('', RedirectView.as_view(url='/user/login/', permanent=False)),  # Redirigir la raíz al login
]

# Añadir la configuración para servir archivos en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



