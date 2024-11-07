from django import forms
from .models import Parametro

class ParametroForm(forms.ModelForm):
    class Meta:
        model = Parametro
        fields = ['nombre_parametro', 'valor_parametro', 'abreviatura_parametro', 'estado_auditoria']
