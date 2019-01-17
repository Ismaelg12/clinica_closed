from django import forms
from core.models import Convenio,Sala,Procedimento,ListaEspera

TRUE_FALSE_CHOICES = (
    (True, 'Sim'),
    (False, 'Não')
)

class ConvenioForm(forms.ModelForm):
    class Meta:
        model =  Convenio
        fields = '__all__'
        widgets = {
            'nome'       : forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
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
    class Meta:
        model =  ListaEspera
        fields = '__all__'
        widgets = {
            'nome'           : forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
            'telefone'       : forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
            'sexo'           : forms.Select(attrs={'class': 'form-control','required': 'true' }),
            'data_nascimento': forms.TextInput(attrs={'class': 'form-control','required': 'true'}),
            'observacao'     : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
        }