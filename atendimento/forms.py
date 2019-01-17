from django import forms
from atendimento.models import Agendamento,Atendimento
from core.models import Procedimento
from controle_usuarios.models import Profissional
class AgendaForm(forms.ModelForm):
    #filtra apenas os profissionais que trabalham como fisioterapeutas
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profissional'].queryset = Profissional.objects.filter(tipo=2)

    class Meta:
        model   = Agendamento
        fields  = '__all__'
        widgets = {
            'data'        : forms.DateInput(attrs={'class': 'form-control','required': 'true'}),
            'hora_inicio' : forms.TimeInput(attrs={'class': 'form-control input-rounded'}),
            'hora_fim'    : forms.TimeInput(attrs={'class': 'form-control','required': 'true'}),
            'sala'        : forms.Select(attrs={'class': 'form-control','required': 'true'}),
            'paciente'    : forms.Select(attrs={'class': 'form-control','required': 'true'}),
            'convenio'    : forms.Select(attrs={'class': 'form-control','required': 'true'}),
            'profissional': forms.Select(attrs={'class': 'form-control','required': 'true'}),
            'telefone'    : forms.TextInput(attrs={'class': 'form-control','required': 'true'}),
           # 'status'      : forms.Select(attrs={'class': 'form-control','readonly':'readonly'}),
            'observacao'  : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
        }
    

class AtendimentoForm(forms.ModelForm):
    class Meta:
        model  = Atendimento
        fields = '__all__'
        widgets = {
            'tipo'              : forms.Select(attrs={'class': 'form-control','onchange':'showDiv(this)'}),
            'paciente'          : forms.Select(attrs={'class': 'form-control',}),
            'data'              : forms.DateInput(attrs={'class': 'form-control','required': 'true'}),
            'procedimento'      : forms.Select(attrs={'class': 'form-control','required': 'true'}),
            'hora_inicio'       : forms.TimeInput(attrs={'class': 'form-control input-rounded','type':'time'}),
            'hora_fim'          : forms.TimeInput(attrs={'class': 'form-control input-rounded','type':'time'}),
            'convenio'          : forms.Select(attrs={'class': 'form-control','required': 'true'}),
            'profissional'          : forms.Select(attrs={'class': 'form-control','required': 'true'}),
            'qp'                : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'diagnostico'       : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'hda'               : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'outras_doencas'    : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'pa'                : forms.TextInput(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'mmHg'              : forms.TextInput(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'bpm'               : forms.TextInput(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'rpm'               : forms.TextInput(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'inspecao'          : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'palpacao'          : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'exame_fisico1'     : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'exame_fisico2'     : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'teste_especifico'  : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'tratamento'        : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'exame_complementar': forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'evolucao'          : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['procedimento'].queryset = Procedimento.objects.none()

        if 'convenio' in self.data:
            try:
                convenio_id = int(self.data.get('convenio'))
                self.fields['procedimento'].queryset = Procedimento.objects.filter(convenio=convenio_id).order_by('nome')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['procedimento'].queryset = self.instance.convenio.procedimento_set.order_by('nome')