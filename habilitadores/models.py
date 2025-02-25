from django.db import models
from parametria.models import Parametro

class HabilitadorCiberseguridad(models.Model):
    codigo = models.AutoField(primary_key=True)
    dimension = models.ForeignKey(Parametro, on_delete=models.CASCADE, related_name='dimension_habilitador', limit_choices_to={'nombre_parametro': 'DIMENSION', 'estado_auditoria': 'activo'})
    dominio = models.ForeignKey(Parametro, on_delete=models.CASCADE, related_name='dominio_habilitador', limit_choices_to={'nombre_parametro': 'DOMINIO', 'estado_auditoria': 'activo'})
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    lineamiento = models.ForeignKey(Parametro, on_delete=models.CASCADE, related_name='lineamiento_habilitador', limit_choices_to={'nombre_parametro': 'LINEAMIENTO', 'estado_auditoria': 'activo'})
    imprescindible = models.ForeignKey(Parametro, on_delete=models.CASCADE, related_name='imprescindible_habilitador', limit_choices_to={'nombre_parametro': 'IMPRESCINDIBLE', 'estado_auditoria': 'activo'})
    entregable = models.BooleanField(default=False)
    observacion = models.TextField(null=True, blank=True)
    estado_auditoria = models.ForeignKey(Parametro, on_delete=models.CASCADE, related_name='estado_auditoria_habilitador', limit_choices_to={'nombre_parametro': 'ESTADO', 'estado_auditoria': 'activo'})
    usuario_auditoria = models.CharField(max_length=50)
    fecha_auditoria = models.DateField(auto_now_add=True)
    JIRA_API_TOKEN = 'ATATT3xFfGF0_7dg6e9Z52MuOCc4clVtUvuaXJ9xWYDp27sHdKiOTgvOITw65GlujMjfHev-Zsphe3wtObJJvc_u3zMVz-kcbIlRiJ_lOz7GUFlNtWUWY4ghUPIr7rL42G9vpngqHUzxtyl6ixbX9IsUp8rl5rPAOI1i_qLXee_tLj4dbVZ3QyA=667CE1A3'
    

    def __str__(self):
        return self.titulo


