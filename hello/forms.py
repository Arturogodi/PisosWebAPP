from django import forms
from hello.models import LogMessage

class LogMessageForm(forms.ModelForm):
    class Meta:
        model = LogMessage
        fields = ("message",)   # NOTE: the trailing comma is required

class PropiedadForm(forms.Form):
    TIPO_CHOICES = [
        ('piso', 'Piso'),
        ('casa', 'Casa'),
        ('chalet', 'Chalet'),
    ]
    tipo = forms.ChoiceField(choices=TIPO_CHOICES, label='Tipo de casa')
    metros = forms.IntegerField(min_value=1, label='Metros cuadrados', widget=forms.NumberInput(attrs={'placeholder': 'Ejemplo: 80'}))
    banos = forms.ChoiceField(choices=[(str(i), str(i)) for i in range(4)], label='Número de baños')
    estado_choices = [
        ('nuevo', 'Nuevo'),
        ('reformado', 'Reformado'),
        ('sin_reformar', 'Sin Reformar'),
    ]
    estado = forms.ChoiceField(choices=estado_choices, label='Estado de la casa')


