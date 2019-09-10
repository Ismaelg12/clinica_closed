from django import forms
from atendimento.models import Atendimento,Guia,Evolucao,TerapiaOcupacional,Psiquiatria,Fisioterapeuta,Anaminese_adulto, Anaminese_crianca, Uroginecologia,Neurologia, Nutricao
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
        #self.fields['procedimento'].queryset = Procedimento.objects.none()
        #self.fields['guia'].queryset = Guia.objects.none()
        """
        if 'convenio' in self.data  and 'paciente' in self.data:
            try:
                convenio_id = int(self.data.get('convenio'))
                paciente_id = int(self.data.get('paciente'))
                self.fields['procedimento'].queryset = Procedimento.objects.filter(convenio=convenio_id).order_by('nome')
                self.fields['guia'].queryset = Guia.objects.filter(paciente=paciente_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['procedimento'].queryset = self.instance.convenio.procedimento_set.order_by('nome')
            self.fields['guia'].queryset = self.instance.paciente.guia_set
        """
    #valida os campos
    
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
        
#mexer so aqui após a elas
class TerapiaOcupacionalForm(forms.ModelForm):
    class Meta:
        model = TerapiaOcupacional
        exclude = ['atendimento']
        widgets ={
            'peso'                : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'gestacao_parto'      : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'aspecto_motor'       : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'aspecto_sensorio'    : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'aspecto_social'      : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'comunicacao'         : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'condulta_terapeutica': forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  

        }


class PsiquiatriaForm(forms.ModelForm):
    class Meta:
        model = Psiquiatria
        exclude = ['atendimento']
        widgets ={
            'queixa'               : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'hma'                  : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'queixa_sintomatica'   : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'hist_medicacao'       : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'ante_psiquiatrico'    : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'ante_medico'          : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'exam_complementar'    : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'observacao'           : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'eixo1'                : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'eixo2'                : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'eixo3'                : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),   
            'eixo4'                : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),   
            'eixo5'                : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),   
            'Condulta_psiquiatrica': forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),   

        }

class FisioterapiaForm(forms.ModelForm):
    class Meta:
        model = Fisioterapeuta
        exclude = ['atendimento']
        widgets ={
            'cid'                  : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'queixa'               : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'has'                  : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),   
            'cardiaca'             : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}), 
            'dm'                   : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}), 
            'hipotireoidismo'      : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}), 
            'neoplasia'            : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'onde_neoplasia'       : forms.TextInput(attrs={'class': 'form-control'}), 
            'tromboflebite'        : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}), 
            'fratura'              : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}), 
            'onde_fratura'         : forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
            'sintese_metalica'     : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),  
            'disturbio'            : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}), 
            'doenca'               : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}), 
            'marca_passo'          : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}), 
            'epifise'              : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}), 
            'sind_raynaud'         : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}), 
            'fotosensibilidade'    : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}), 
            'gravidez'             : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}), 
            'outro'                : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'exam_complementar'    : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'exam_fisico'          : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'esquema_corporal'     : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'Condu_fisioterapica'  : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  

        }

class AnamineseAdultoForm(forms.ModelForm):
    class Meta:
        model = Anaminese_adulto
        exclude = ['atendimento']
        widgets ={ 
            'queixa'               : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'psic_anterior'        : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control'}),   
            'psiq_anterior'        : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control'}), 
            'encaminhado_por'      : forms.TextInput(attrs={'class': 'form-control'}),
            'outro_profissional'   : forms.TextInput(attrs={'class': 'form-control'}), 
            'uso_medicacao'        : forms.TextInput(attrs={'class': 'form-control'}),
            'med_psiquiatrico'     : forms.TextInput(attrs={'class': 'form-control'}), 
            'reacao_fisiolo'       : forms.TextInput(attrs={'class': 'form-control'}), 
            'hist_doencas'         : forms.TextInput(attrs={'class': 'form-control'}), 
            'hist_dificuldade'     : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'dinamica_fam'         : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'fato_marcante'        : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'trauma'               : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'afetivo'              : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'vida_sexual'          : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'amizade'              : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'lazer'                : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'rotina'               : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'escolar'              : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}), 
            'profissional2'        : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'pessoal'              : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'familiar'             : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'plano_futuro'         : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),  
            'expectativa'          : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'dificul_pessoal'      : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'caracteristica'       : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'meta'                 : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'postura_geral'        : forms.TextInput(attrs={'class': 'form-control'}), 
            'cuidado_pessoal'      : forms.TextInput(attrs={'class': 'form-control'}), 
            'fluencia'             : forms.TextInput(attrs={'class': 'form-control'}), 
            'organizacao'          : forms.TextInput(attrs={'class': 'form-control'}), 
            'tique'                : forms.TextInput(attrs={'class': 'form-control'}), 
            'observacao'           : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),

        }


class AnamineseCriancaForm(forms.ModelForm):
    class Meta:
        model = Anaminese_crianca
        exclude = ['atendimento']
        widgets ={ 
            'responsavel'          : forms.TextInput(attrs={'class': 'form-control'}),
            'n_irmaos'             : forms.TextInput(attrs={'class': 'form-control'}),
            'posicao_familiar'     : forms.TextInput(attrs={'class': 'form-control'}),
            'matrimonio'           : forms.Select(choices=MATRIMONIO,attrs={'class': 'form-control','required': 'true'}),
            'reacao_1'             : forms.TextInput(attrs={'class': 'form-control'}),
            'caso_separado'        : forms.TextInput(attrs={'class': 'form-control'}),
            'filho'                : forms.Select(choices=FILHO,attrs={'class': 'form-control','required': 'true'}),
            'crianca_ciente'       : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'reacao_2'             : forms.TextInput(attrs={'class': 'form-control'}),
            'queixa'               : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'tempo'                : forms.TextInput(attrs={'class': 'form-control'}),
            'frequencia'           : forms.TextInput(attrs={'class': 'form-control'}),
            'consequencia'         : forms.TextInput(attrs={'class': 'form-control'}),
            'atitude_Pais'         : forms.TextInput(attrs={'class': 'form-control'}),
            'esforco'              : forms.TextInput(attrs={'class': 'form-control'}),
            'outro_profissional'   : forms.TextInput(attrs={'class': 'form-control'}),
            'medicacoes'           : forms.TextInput(attrs={'class': 'form-control'}),
            'ativ_ocupacional'     : forms.TextInput(attrs={'class': 'form-control'}),
            'gestacao'             : forms.Select(choices=GESTACAO,attrs={'class': 'form-control','required': 'true'}),
            'saude_mae'            : forms.Select(choices=SAUDE_MAE,attrs={'class': 'form-control','required': 'true'}),
            'Parto'                : forms.Select(choices=TIPO_PARTO,attrs={'class': 'form-control','required': 'true'}),
            'idade'                : forms.TextInput(attrs={'class': 'form-control'}),
            'enjoou'               : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'tempo_1'              : forms.TextInput(attrs={'class': 'form-control'}),
            'gav_desejada'         : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'abortos'              : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'qnt_abortos'          : forms.TextInput(attrs={'class': 'form-control'}),
            'compl_gravidez'       : forms.TextInput(attrs={'class': 'form-control'}),
            'denc_concepcao'       : forms.TextInput(attrs={'class': 'form-control'}),
            'amamentacao'          : forms.Select(choices=AMAMENTACAO,attrs={'class': 'form-control','required': 'true'}),
            'ate_idade1'           : forms.TextInput(attrs={'class': 'form-control'}),
            'mamadeira'            : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'ate_idad2'            : forms.TextInput(attrs={'class': 'form-control'}),
            'alimentacao'          : forms.TextInput(attrs={'class': 'form-control'}),
            'desenv_esperado'      : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'sorriu_idade'         : forms.TextInput(attrs={'class': 'form-control'}),
            'engatinhou_idade'     : forms.TextInput(attrs={'class': 'form-control'}),
            'ficou_pe'             : forms.TextInput(attrs={'class': 'form-control'}),
            'andou_idade'          : forms.TextInput(attrs={'class': 'form-control'}),
            'correu'               : forms.TextInput(attrs={'class': 'form-control'}),
            'braco'                : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'palavras'             : forms.TextInput(attrs={'class': 'form-control'}),
            'atraso_fala'          : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'troca_letra'          : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'qual1'                : forms.TextInput(attrs={'class': 'form-control'}),
            'dificul_esfincter'    : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'contro_esfincter'     : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'idade2'               : forms.TextInput(attrs={'class': 'form-control'}),
            'mania'                : forms.TextInput(attrs={'class': 'form-control'}),
            'enurese_noturna'      : forms.TextInput(attrs={'class': 'form-control'}),
            'desenv_afetado'       : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'dificul_fala'         : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'qual4'                : forms.TextInput(attrs={'class': 'form-control'}),
            'visao'                : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'qual5'                : forms.TextInput(attrs={'class': 'form-control'}),
            'locomocao'            : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'qual6'                : forms.TextInput(attrs={'class': 'form-control'}),
            'avds'                 : forms.TextInput(attrs={'class': 'form-control'}),
            'banha_so'             : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'escova_so'            : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'usa_banheiro_so'      : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'precisa_auxilio'      : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'retirada_fruda'       : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'intervencao'          : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'chora_fabi'           : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'recus_auxililo'       : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'resistencia'          : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'bem_escola'           : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'gosta_estudar'        : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'estudam_criança'      : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'orientacao_dever'     : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'quem_ajuda'           : forms.TextInput(attrs={'class': 'form-control'}),
            'tempo_ajuda'          : forms.TextInput(attrs={'class': 'form-control'}),
            'gosta_professora'     : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'nota_baixa'           : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'materia'              : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'qual7'                : forms.TextInput(attrs={'class': 'form-control'}),
            'idade_escola'         : forms.TextInput(attrs={'class': 'form-control'}),
            'destro'               : forms.TextInput(attrs={'class': 'form-control'}),
            'outra_escola'         : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'qual8'                : forms.TextInput(attrs={'class': 'form-control'}),
            'mortivo_trans'        : forms.TextInput(attrs={'class': 'form-control'}),
            'repetiu_serie'        : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'lingua_estrangeira'   : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'qual_ling'            : forms.TextInput(attrs={'class': 'form-control'}),    
            'esporte'              : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'qual_esporte'         : forms.TextInput(attrs={'class': 'form-control'}),
            'danca'                : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'qual_danca'            : forms.TextInput(attrs={'class': 'form-control'}),  
            'intru_musical'        : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'qual_inst'            : forms.TextInput(attrs={'class': 'form-control'}),  
            'outra_ativi'          : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'qual_outra'            : forms.TextInput(attrs={'class': 'form-control'}), 
            'faz_amigo'            : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'adaptacao'            : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'compa_brincadeira'    : forms.TextInput(attrs={'class': 'form-control'}),
            'mesmo_sexo'           : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'sexo_oposto'          : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'mesma_idade'          : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'mais_nova'            : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'mais_velha'           : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'tv'                   : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'musica'               : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'leitura'              : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'colecao'              : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'computador'           : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'outra_distracao'      : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'obediente'            : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'independente'         : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'comunicativo'         : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'agressivo'            : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'cooperador'           : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'outra_atitude'        : forms.TextInput(attrs={'class': 'form-control'}),
            'tranquilo'            : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'seguro'               : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'ancioso'              : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'alegre'               : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'emotivo'              : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'queixoso'             : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'outra_emocao'         : forms.TextInput(attrs={'class': 'form-control'}),
            'insonia'              : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'pesadelo'             : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'hipersonia'           : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'dorme_sozinho'        : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'dorme_pais'           : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'divide_quarto'        : forms.TextInput(attrs={'class': 'form-control'}),
            'perturbacao'          : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'habito_especial'      : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'disciplina_pai'       : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'contrariado'          : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'histo_doenca'         : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'freque_doenca'        : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'idade3'               : forms.TextInput(attrs={'class': 'form-control'}),
            'qual_neurologico'     : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'acomp_psicologico'    : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'outro_acompanha'      : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'uso_medicamento'      : forms.TextInput(attrs={'class': 'form-control'}),
            'outra_ocorrencia'     : forms.TextInput(attrs={'class': 'form-control'}),
            'probl_mental'         : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'grau_parentesco'      : forms.TextInput(attrs={'class': 'form-control'}),
            'dificul_apresentada'  : forms.TextInput(attrs={'class': 'form-control'}),
            'relac_pai'            : forms.TextInput(attrs={'class': 'form-control'}),
            'relac_irmao'          : forms.TextInput(attrs={'class': 'form-control'}),
            'ponto_posi'           : forms.TextInput(attrs={'class': 'form-control'}),
            'ponto_nega'           : forms.TextInput(attrs={'class': 'form-control'}),
            'terapia'              : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'Observacao'           : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),

        }


class UroginecologiaForm(forms.ModelForm):
    class Meta:
        model = Uroginecologia
        exclude = ['atendimento']
        widgets ={ 
            'encaminhado_por'      : forms.TextInput(attrs={'class': 'form-control'}),
            'medico_responsavel'   : forms.TextInput(attrs={'class': 'form-control'}),
            'diagnostico_origem'   : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'queixa'               : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'hda'                  : forms.TextInput(attrs={'class': 'form-control'}),
            'hpp'                  : forms.TextInput(attrs={'class': 'form-control'}),
            'antece_cirurgico'     : forms.TextInput(attrs={'class': 'form-control'}),
            'antece_familiar'      : forms.TextInput(attrs={'class': 'form-control'}),
            'uso_medicacao'        : forms.TextInput(attrs={'class': 'form-control'}),
            'incont_urinaria'      : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'como_perde'           : forms.TextInput(attrs={'class': 'form-control'}),
            'quanto_perde'         : forms.TextInput(attrs={'class': 'form-control'}),
            'como_urina'           : forms.TextInput(attrs={'class': 'form-control'}),
            'frequencia_perda'     : forms.TextInput(attrs={'class': 'form-control'}),
            'usa_frauda'           : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'frequencia_urina'     : forms.TextInput(attrs={'class': 'form-control'}),
            'funcao_intestinal'    : forms.TextInput(attrs={'class': 'form-control'}),
            'menarca'              : forms.TextInput(attrs={'class': 'form-control'}),
            'contracepcao_tipo'    : forms.TextInput(attrs={'class': 'form-control'}),
            'menopausa'            : forms.TextInput(attrs={'class': 'form-control'}),    
            'gpca'                 : forms.TextInput(attrs={'class': 'form-control'}),
            'episotomia'           : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'forceps'              : forms.Select(choices=OP_CHOICES,attrs={'class': 'form-control','required': 'true'}),
            'tempo_parto'          : forms.TextInput(attrs={'class': 'form-control'}),
            'complicacao'          : forms.TextInput(attrs={'class': 'form-control'}),
            'Cirurg_ginecologica'  : forms.TextInput(attrs={'class': 'form-control'}),
            'dst'                  : forms.TextInput(attrs={'class': 'form-control'}),
            'infec_urinaria'       : forms.TextInput(attrs={'class': 'form-control'}),
            'exame_complementar'   : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'exame_fisico'         : forms.Textarea(attrs={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'afa'                  : forms.TextInput(attrs={'class': 'form-control'}),
            'perfect'              : forms.TextInput(attrs={'class': 'form-control'}),
        }


class NeurologiaForm(forms.ModelForm):
    class Meta:
        model = Neurologia
        exclude = ['atendimento']
        widgets ={ 
            'diag_medico'      : forms.TextInput(attrs ={'class': 'form-control'}),
            'medico'           : forms.TextInput(attrs ={'class': 'form-control'}),
            'diag_fisio'       : forms.Textarea(attrs  ={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'distur_assoc'     : forms.Textarea(attrs  ={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'hda'              : forms.Textarea(attrs  ={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'exame'            : forms.Textarea(attrs  ={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'cirurgia'         : forms.Textarea(attrs  ={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'dispo_auxi'       : forms.Textarea(attrs  ={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'capacidade'       : forms.Textarea(attrs  ={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'pre_test'         : forms.Textarea(attrs  ={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'aval_video'       : forms.Textarea(attrs  ={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'aval_postural'    : forms.Textarea(attrs  ={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'adm_1'            : forms.TextInput(attrs ={'class': 'form-control'}),
            'adm_2'            : forms.TextInput(attrs ={'class': 'form-control'}),
            'adm_3'            : forms.TextInput(attrs ={'class': 'form-control'}),
            'adm_4'            : forms.TextInput(attrs ={'class': 'form-control'}),
            'adm_5'            : forms.TextInput(attrs ={'class': 'form-control'}),
            'adm_6'            : forms.TextInput(attrs ={'class': 'form-control'}),
            'adm_7'            : forms.TextInput(attrs ={'class': 'form-control'}),
            'adm_8'            : forms.TextInput(attrs ={'class': 'form-control'}),
            'articular_1'      : forms.TextInput(attrs ={'class': 'form-control'}),
            'articular_2'      : forms.TextInput(attrs ={'class': 'form-control'}),
            'articular_3'      : forms.TextInput(attrs ={'class': 'form-control'}),
            'articular_4'      : forms.TextInput(attrs ={'class': 'form-control'}),
            'articular_5'      : forms.TextInput(attrs ={'class': 'form-control'}),
            'articular_6'      : forms.TextInput(attrs ={'class': 'form-control'}),
            'articular_7'      : forms.TextInput(attrs ={'class': 'form-control'}),
            'articular_8'      : forms.TextInput(attrs ={'class': 'form-control'}),
            'encurtamento_1'   : forms.TextInput(attrs ={'class': 'form-control'}),
            'encurtamento_2'   : forms.TextInput(attrs ={'class': 'form-control'}),
            'encurtamento_3'   : forms.TextInput(attrs ={'class': 'form-control'}),
            'encurtamento_4'   : forms.TextInput(attrs ={'class': 'form-control'}),
            'encurtamento_5'   : forms.TextInput(attrs ={'class': 'form-control'}),
            'encurtamento_6'   : forms.TextInput(attrs ={'class': 'form-control'}),
            'encurtamento_7'   : forms.TextInput(attrs ={'class': 'form-control'}),
            'encurtamento_8'   : forms.TextInput(attrs ={'class': 'form-control'}),
            'tonus_1'          : forms.TextInput(attrs ={'class': 'form-control'}),
            'tonus_2'          : forms.TextInput(attrs ={'class': 'form-control'}),
            'tonus_3'          : forms.TextInput(attrs ={'class': 'form-control'}),
            'tonus_4'          : forms.TextInput(attrs ={'class': 'form-control'}),
            'tonus_5'          : forms.TextInput(attrs ={'class': 'form-control'}),
            'tonus_6'          : forms.TextInput(attrs ={'class': 'form-control'}),
            'tonus_7'          : forms.TextInput(attrs ={'class': 'form-control'}),
            'tonus_8'          : forms.TextInput(attrs ={'class': 'form-control'}),
            'forca_1'          : forms.TextInput(attrs ={'class': 'form-control'}),
            'forca_2'          : forms.TextInput(attrs ={'class': 'form-control'}),
            'forca_3'          : forms.TextInput(attrs ={'class': 'form-control'}),
            'forca_4'          : forms.TextInput(attrs ={'class': 'form-control'}),
            'forca_5'          : forms.TextInput(attrs ={'class': 'form-control'}),
            'forca_6'          : forms.TextInput(attrs ={'class': 'form-control'}),
            'forca_7'          : forms.TextInput(attrs ={'class': 'form-control'}),
            'forca_8'          : forms.TextInput(attrs ={'class': 'form-control'}),
        }

class NutricaoForm(forms.ModelForm):
    class Meta:
        model = Nutricao
        exclude = ['atendimento']
        widgets ={ 
            'qpdhda'                : forms.Textarea(attrs  ={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'exam_fisico'           : forms.Textarea(attrs  ={'class': 'form-control','cols' : "10", 'rows': "3",}),
            'exam_complementar'     : forms.Textarea(attrs  ={'class': 'form-control','cols' : "10", 'rows': "3",}),
            
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
        self.fields['profissional'].queryset = Profissional.prof_objects.filter(tipo=2)
        self.fields['procedimento'].queryset = Procedimento.objects.none()
        self.fields['paciente'].label_from_instance = self.paciente_label
        
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
            'numero'      : forms.NumberInput(attrs={'class': 'form-control'}),
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


    #verifica se o paciente tem mais de 1 guia para um mesmo profissional
    def clean(self):
        data  = self.cleaned_data
        profissional = data['profissional']
        paciente     = data['paciente']
        if Guia.objects.filter(profissional__id=profissional[0].id,
            paciente__id=paciente.id,ativo=True).exists():
            raise forms.ValidationError('Esse Profissional já possui 1 Guia com esse paciente')
        return data
    
        