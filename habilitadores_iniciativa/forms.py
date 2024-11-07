from django import forms
from .models import HabilitadoresIniciativaCabecera, HabilitadoresIniciativaDetalle

# Formulario para la cabecera de la iniciativa
class HabilitadoresIniciativaCabeceraForm(forms.ModelForm):
    class Meta:
        model = HabilitadoresIniciativaCabecera
        fields = ['cod_jira', 'squad', 'po', 'iniciativa', 'analista_seguridad','quarter']

# Formulario para los detalles de la iniciativa
class HabilitadoresIniciativaDetalleForm(forms.ModelForm):
    class Meta:
        model = HabilitadoresIniciativaDetalle
        fields = ['habilitador', 'estado_cumplimiento', 'exception', 'observacion']
        widgets = {
            'observacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'style': 'resize:none; height: 30px;'}),
            'exception': forms.Textarea(attrs={'class': 'form-control', 'rows': 1, 'style': 'resize:none; height: 30px;'}),
        }



