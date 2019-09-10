from django import forms
from core.models import Convenio,Sala,Procedimento,ListaEspera
from controle_usuarios.models import Profissional
from django.core.exceptions import ValidationError


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
            'codigo'    : forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
            'nome'      : forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
            'convenio'  : forms.Select(attrs={'class':'selectpicker','data-style':'select-with-transition',
                'data-size':5,'required': 'true' }),
            'valor'     : forms.NumberInput(attrs={'class': 'form-control','required': 'true','step': "0.01"}),
            'ativo'     : forms.Select(choices=TRUE_FALSE_CHOICES,attrs={'class': 'form-control','required': 'true','step': "0.01"}),
            'descricao' : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
        }
    
    
    #valida se tem registros duplicados no banco
    def clean(self):
        cod  = self.cleaned_data['codigo']
        conv = self.cleaned_data['convenio']
        if Procedimento.objects.filter(codigo=cod,convenio__nome__startswith=conv,id=self.instance.id).exists():
            pass
        elif Procedimento.objects.filter(codigo=cod,convenio__nome__startswith=conv).exists(): 
            raise ValidationError('Procedimento Já existe na base da dados!')
        return None


class ListaEsperaForm(forms.ModelForm):
    profissional = forms.ModelMultipleChoiceField(
        queryset = Profissional.prof_objects.all(),
        widget   =   forms.SelectMultiple(attrs={'class':'selectpicker',
        'data-style':'select-with-transition','data-size':7,
        'data-live-search':'true','multiple':'multiple','title':'Selecione um profissional'})
    )
    
    class Meta:
        model =  ListaEspera
        fields = '__all__'
        widgets = {
            'nome'           : forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
            'idade'          : forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
            'telefone'       : forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
            'sexo'           : forms.Select(attrs={'class': 'form-control','required': 'true' }),
            'turno'          : forms.Select(attrs={'class': 'form-control','required': 'true' }),
            'especialidade'  : forms.Select(attrs={'class': 'form-control','required': 'true' }),
            #'profissional'   : forms.Select(attrs={'class': 'form-control','required': 'true' }),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control','required': 'true'}),
            'observacao'     : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "1",}), 
        }
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profissional'].queryset = Profissional.prof_objects.none()

        if 'especialidade' in self.data:
            try:
                especialidade = int(self.data.get('especialidade'))
                print(especialidade,'teste')
                self.fields['profissional'].queryset = Profissional.prof_objects.filter(area_atuacao=especialidade).order_by('nome')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            #print('instancia do profissional',self.instance.pk,self.instance.nome,self.instance.especialidade)
            self.fields['profissional'].queryset = Profissional.prof_objects.filter(area_atuacao=self.instance.especialidade).order_by('nome')
        """
