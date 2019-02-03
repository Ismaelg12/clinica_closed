from django import forms
from core.models import Convenio,Sala,Procedimento,ListaEspera
from controle_usuarios.models import Profissional

TRUE_FALSE_CHOICES = (
    (True, 'Sim'),
    (False, 'Não')
)

class ConvenioForm(forms.ModelForm):
    class Meta:
        model =  Convenio
        fields = '__all__'
        widgets = {
            'nome'       : forms.Select(attrs={'class':'selectpicker',
            'data-style':'select-with-transition','data-size':7}),
            'ativo'      : forms.Select(choices=TRUE_FALSE_CHOICES,attrs={'class': 'form-control','required': 'true' }),
        }


class SalaForm(forms.ModelForm):
    class Meta:
        model =  Sala
        fields = '__all__'
        widgets = {
            'nome'      : forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
            'descricao' : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
        }

class ProcedimentoForm(forms.ModelForm):
    class Meta:
        model =  Procedimento
        fields = '__all__'
        widgets = {
            'codigo'    : forms.NumberInput(attrs={'class': 'form-control','required': 'true' }),
            'nome'      : forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
            'convenio'  : forms.Select(attrs={'class': 'form-control','required': 'true' }),
            'valor'     : forms.NumberInput(attrs={'class': 'form-control','required': 'true','step': "0.01"}),
            'ativo'     : forms.Select(choices=TRUE_FALSE_CHOICES,attrs={'class': 'form-control','required': 'true','step': "0.01"}),
            'descricao' : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
        }
class ListaEsperaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profissional'].queryset = Profissional.objects.none()
        """
        if 'especialidade' in self.data:
            try:
                especialidade = int(self.data.get('especialidade'))
                print(especialidade)
                self.fields['profissional'].queryset = Procedimento.objects.filter(area_atuacao=especialidade).order_by('nome')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['profissional'].queryset = self.instance.especialidade.profissional_set.order_by('nome')
        """
    class Meta:
        model =  ListaEspera
        fields = '__all__'
        widgets = {
            'nome'           : forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
            'telefone'       : forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
            'sexo'           : forms.Select(attrs={'class': 'form-control','required': 'true' }),
            'especialidade'  : forms.Select(attrs={'class': 'form-control','required': 'true' }),
            'profissional'   : forms.Select(attrs={'class': 'form-control','required': 'true' }),
            'data_nascimento': forms.TextInput(attrs={'class': 'form-control','required': 'true'}),
            'observacao'     : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
        }