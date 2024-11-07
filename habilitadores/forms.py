from django import forms
from .models import HabilitadorCiberseguridad
from parametria.models import Parametro

class HabilitadorCiberseguridadForm(forms.ModelForm):
    class Meta:
        model = HabilitadorCiberseguridad
        fields = ['dimension', 'dominio', 'lineamiento', 'imprescindible', 'titulo', 'descripcion', 'entregable', 'observacion']

    def __init__(self, *args, **kwargs):
        super(HabilitadorCiberseguridadForm, self).__init__(*args, **kwargs)

        self.fields['dimension'].queryset = Parametro.objects.filter(nombre_parametro='DIMENSION', estado_auditoria='activo')
        self.fields['dominio'].queryset = Parametro.objects.filter(nombre_parametro='DOMINIO', estado_auditoria='activo')
        self.fields['lineamiento'].queryset = Parametro.objects.filter(nombre_parametro='LINEAMIENTO', estado_auditoria='activo')
        self.fields['imprescindible'].queryset = Parametro.objects.filter(nombre_parametro='IMPRESCINDIBLE', estado_auditoria='activo')

        # Muestra el valor del parámetro en los combobox
        self.fields['dimension'].label_from_instance = lambda obj: obj.valor_parametro
        self.fields['dominio'].label_from_instance = lambda obj: obj.valor_parametro
        self.fields['lineamiento'].label_from_instance = lambda obj: obj.valor_parametro
        self.fields['imprescindible'].label_from_instance = lambda obj: obj.valor_parametro
