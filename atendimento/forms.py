from django import forms
from atendimento.models import Evolucao, Avaliacao, Guia, Atendimento,Convenio
from core.models import Procedimento
from pacientes.models import Paciente
from controle_usuarios.models import Profissional
from core.utils import *    

         
OP_CHOICES = (
    ('', 'Escolha Um Opçao'),
    (True, 'Sim'),
    (False, 'Não')
)

class AtendimentoForm(forms.ModelForm):
    class Meta:
        model  = Atendimento
        fields = '__all__'
        widgets = {
            'tipo'              : forms.Select(attrs={'class': 'form-control','onchange':'showDiv(this)'}),
            'paciente'          : forms.Select(attrs={'class': 'form-control',}),
            'data'              : forms.DateInput(attrs={'class': 'form-control','required': 'true'}),
            'procedimento'      : forms.Select(attrs={'class': 'form-control',}),
            'hora_inicio'       : forms.TimeInput(attrs={'class': 'form-control input-rounded','type':'time'}),
            'hora_fim'          : forms.TimeInput(attrs={'class': 'form-control input-rounded','type':'time'}),
            'convenio'          : forms.Select(attrs={'class':'selectpicker','data-style':'select-with-transition',
                'data-size':7,'data-live-search':'true','required': 'true'}),
            'guia'              : forms.Select(attrs={'class': 'form-control',}),
            'profissional'      : forms.Select(attrs={'class': 'form-control',}),
            'valor'             : forms.NumberInput(attrs={'class': 'form-control','placeholder':'R$ 0.00'}),  
            'evolucao'          : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profissional'].queryset = Profissional.objects.filter(tipo=2)
    
    def clean(self):
        data  = self.cleaned_data
        if data.get('convenio', None).nome !='particular':
            if data.get('procedimento', None) ==  None and data.get('guia', None) ==None:
                print(data.get('procedimento', None))
                raise forms.ValidationError('Preencha os campos de Procedimento e Guia Por Favor')
        return data
    


#forms de fichas 

class EvolucaoForm(forms.ModelForm):
    class Meta:
        model = Evolucao
        exclude = ['atendimento']
        widgets ={
            'evolucao'          : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "7",}),  
            

        }

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        exclude = ['atendimento']
        widgets ={
            'queixa'            : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "6",}),
            'familia'           : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "6",}),
            'patologico'        : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "6",}),
            'social'            : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "6",}),
            'condulta'          : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "6",}),
            
        }

class GuiaForm(forms.ModelForm):
    profissional = forms.ModelMultipleChoiceField(
        queryset = Profissional.objects.all(),
        widget   =   forms.SelectMultiple(attrs={'class':'selectpicker',
        'data-style':'select-with-transition','data-size':7,
        'data-live-search':'true','multiple':'multiple','title':'selecione o profisional'})
    )

    #filtra apenas os profissionais que trabalham como fisioterapeutas
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset     = Paciente.objects.select_related('convenio'
        ).exclude(convenio__nome='particular')
        self.fields['profissional'].queryset = Profissional.prof_objects.filter(tipo=2)
        self.fields['procedimento'].queryset = Procedimento.objects.none()
        self.fields['paciente'].label_from_instance = self.paciente_label
        self.fields['convenio'].queryset     = Convenio.objects.exclude(nome='particular')

        if 'convenio' in self.data:
            try:
                convenio_id = int(self.data.get('convenio'))
                self.fields['procedimento'].queryset = Procedimento.objects.filter(
                    convenio=convenio_id).order_by('nome')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['procedimento'].queryset = self.instance.convenio.procedimento_set.order_by('nome')

    #metodo para override de labels do pacientes
    @staticmethod
    def paciente_label(self):
        return str(self.nome) + '.....  ' + self.convenio.nome
    class Meta:
        model = Guia
        fields = '__all__'
        widgets = {
            'numero'      : forms.TextInput(attrs={'class': 'form-control'}),
            'convenio'    : forms.Select(attrs={'class':'selectpicker',
            'data-style':'select-with-transition','data-size':7,'data-live-search':'true'}),
            'paciente'    : forms.Select(attrs={'class':'selectpicker',
            'data-style':'select-with-transition','data-size':7,'data-live-search':'true'}),
            'quantidade'  : forms.NumberInput(attrs={'class': 'form-control'}),
            'qtdautorizada'  : forms.NumberInput(attrs={'class': 'form-control'}),
            'validade'    : forms.DateInput(attrs={'class': 'form-control'}),
            'data_autorizacao': forms.DateInput(attrs={'class': 'form-control'}),
            'tipo_guia'    : forms.Select(attrs={'class':'selectpicker','data-style':'select-with-transition',
            'data-size':7,'required': 'true'}),
            'procedimento'    : forms.Select(attrs={'class':'form-control','required': 'true'}),
            'status'    : forms.Select(attrs={'class':'selectpicker','data-style':'select-with-transition',
            'data-size':7,'required': 'true'}),
            'ativo': forms.Select(choices=OP_CHOICES,attrs={'class': 'selectpicker','required': 'true',
                'data-style':'select-with-transition','data-size':7}),
        }


    def clean(self):
        data = self.cleaned_data
        #print(Guia.objects.filter(numero=data.get('numero', None)),'exists')
        if Guia.objects.filter(numero=data.get('numero', None),id=self.instance.id).exists():
            pass
        elif Guia.objects.filter(numero=data.get('numero', None)).exists():
            raise forms.ValidationError('Guia já Existente na Base de Dados')

    #verifica se o paciente tem mais de 1 guia para um mesmo profissional
    """
    def clean(self):
        data  = self.cleaned_data
        profissional = data['profissional']
        paciente     = data['paciente']
        if Guia.objects.filter(profissional__id=profissional[0].id,
            paciente__id=paciente.id,ativo=True).exists():
            raise forms.ValidationError('Esse Profissional já possui 1 Guia com esse paciente')
        return data
    """
    
        