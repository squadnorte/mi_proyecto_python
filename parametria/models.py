from django.db import models
from django.contrib.auth.models import User  # Para asociar el usuario logueado
from django.utils import timezone

class Parametro(models.Model):
    codigo_parametro = models.AutoField(primary_key=True)
    nombre_parametro = models.CharField(max_length=100)
    valor_parametro = models.CharField(max_length=255)
    abreviatura_parametro = models.CharField(max_length=50)
    usuario_auditoria = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    estado_auditoria = models.CharField(max_length=10, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], default='activo')
    fecha_auditoria = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre_parametro

