from django import forms
from agenda.models import Agendamento
from controle_usuarios.models import Profissional
from pacientes.models import Paciente

OP_CHOICES = (
    ('', 'Escolha Um Opçao'),
    (True, 'Sim'),
    (False, 'Não')
)

class AgendaForm(forms.ModelForm):
    #filtra apenas os profissionais que trabalham como fisioterapeutas
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profissional'].queryset = Profissional.objects.filter(tipo=2,ativo=True)
        self.fields['paciente'].label_from_instance = self.paciente_label
        
    #metodo para override de labels do pacientes
    @staticmethod
    def paciente_label(self):
        return str(self.nome[:30]) + ' -- ' + self.convenio.nome +'...  ' + self.telefone

    class Meta:
        model   = Agendamento
        fields  = '__all__'
        widgets = {
            'data'        : forms.DateInput(attrs={'class': 'form-control','required': 'true'}),
            'hora_inicio' : forms.TimeInput(attrs={'class': 'form-control input-rounded'}),
            'hora_fim'    : forms.TimeInput(attrs={'class': 'form-control','required': 'true'}),
            'sala'        : forms.Select(attrs={'class':'selectpicker','data-style':'select-with-transition',
                'data-size':7,'data-live-search':'true'}),
            'paciente'    : forms.Select(attrs={'class':'selectpicker','data-style':'select-with-transition',
                'data-size':7,'data-live-search':'true','required': 'true'}),
            'convenio'    : forms.Select(attrs={'class':'selectpicker',
            'data-style':'select-with-transition','data-size':7,'data-live-search':'true'}),
            'profissional': forms.Select(attrs={'class':'selectpicker','data-style':'select-with-transition',
                'data-size':7,'data-live-search':'true','required': 'true'}),
            'telefone'    : forms.TextInput(attrs={'class': 'form-control','required': 'true'}),
            'status'      : forms.Select(attrs={'class': 'selectpicker','data-style':'select-with-transition', 'required':'True'}),
            'observacao'  : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'valor'       : forms.TextInput(attrs={'class': 'form-control'}),
            'pago'        : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'pacote'      : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}), 
        }
    
    def clean(self):
        data = self.cleaned_data
        print( data.get('hora_inicio', None), data.get('hora_fim', None))
        if data.get('hora_inicio', None) >= data.get('hora_fim', None):
            raise forms.ValidationError('Corrija o horário')
      
    """
    def clean_profissional(self):
        data = self.cleaned_data
        if data.get('profissional', None) == None:
            raise forms.ValidationError('Campo é obrigatório')
    """
