from django.db import models

class Usuario(models.Model):
    codigo_usuario = models.AutoField(primary_key=True)
    codigo_empresa = models.IntegerField()
    codigo_rol = models.IntegerField()
    nombre_usuario = models.CharField(max_length=50)
    direccion_usuario = models.CharField(max_length=100)
    email_usuario = models.EmailField(max_length=50)
    telefono_usuario = models.CharField(max_length=80)
    nomen_usuario = models.CharField(max_length=80)  # Nuevo campo
    clave_usuario = models.CharField(max_length=250)
    usuario_auditoria = models.CharField(max_length=50)
    fecha_auditoria = models.DateField()
    estado_auditoria = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nombre_usuario

