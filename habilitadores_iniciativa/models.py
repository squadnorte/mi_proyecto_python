from django.db import models
from habilitadores.models import HabilitadorCiberseguridad
from itsdangerous import URLSafeSerializer
from django.conf import settings

class HabilitadoresIniciativaCabecera(models.Model):
    codigo = models.AutoField(primary_key=True)
    cod_jira = models.CharField(max_length=50)
    squad = models.CharField(max_length=20)
    po = models.CharField(max_length=100)
    iniciativa = models.CharField(max_length=500)
    analista_seguridad = models.CharField(max_length=50)
    usuario_auditoria = models.CharField(max_length=50)
    fecha_auditoria = models.DateField(auto_now_add=True)
    estado_auditoria = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')])
    quarter = models.CharField(max_length=50)

    @property
    def id_cifrado(self):
        # Utilizar una clave secreta de settings.py para cifrar el código
        serializer = URLSafeSerializer(settings.ITS_DANGEROUS_SECRET_KEY)
        return serializer.dumps(self.codigo)
    


class HabilitadoresIniciativaDetalle(models.Model):
    codigo = models.AutoField(primary_key=True)
    cabecera = models.ForeignKey(HabilitadoresIniciativaCabecera, on_delete=models.CASCADE)
    habilitador = models.ForeignKey(HabilitadorCiberseguridad, on_delete=models.CASCADE)
    estado_cumplimiento = models.CharField(max_length=50)
    exception = models.CharField(max_length=50, null=True, blank=True)
    observacion = models.TextField(max_length=2000, null=True, blank=True)
    estado_auditoria = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')])
    usuario_auditoria = models.CharField(max_length=50)
    fecha_auditoria = models.DateField(auto_now_add=True)



