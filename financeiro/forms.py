from django import forms
from financeiro.models import *



class ContaReceberForm(forms.ModelForm):
    class Meta:
        model = ContaReceber
        fields = ['forma_pagamento','valor_total_pago','valor_pago_dinheiro','valor_pago_cartao', 'desconto', ]
        widgets = {
            'forma_pagamento'       :forms.Select(attrs={'class':'selectpicker',
            'data-style'            :'select-with-transition','data-size':7}),
            'recebido_por'          :forms.Select(attrs={'class':'selectpicker',
            'data-style'            :'select-with-transition','data-size':7}),
            'desconto'              :forms.NumberInput(attrs={'class': 'form-control','placeholder':'R$ 0,00'}),
            'valor_pago_dinheiro'   :forms.NumberInput(attrs={'class': 'form-control','placeholder':'R$ 0,00'}),
            'valor_total_pago'      :forms.NumberInput(attrs={'class': 'form-control','placeholder':'R$ 0,00'}),
            'valor_pago_cartao'     :forms.NumberInput(attrs={'class': 'form-control','placeholder':'R$ 0,00'}),
        }
    """
    def __init__(self, *args, **kwargs):
        super(ContaReceberForm, self).__init__(*args, **kwargs)
        #se profissional/atendente logado ele seta o tipo de recepção do pagamento
        if Profissional.prof_objects.filter(tipo=2).exists():
            self.initial['receptor'] = 'PF'
        else:
            self.initial['receptor'] = 'RC'
    """


class ContaPagarForm(forms.ModelForm):
    class Meta:
        model = ContaPagar
        fields = '__all__'
        widgets = {
            'data':forms.DateInput(attrs={'class': 'form-control','placeholder':'dd/mm/aaaa','data-language': 'pt'}),
            'valor_total':forms.TextInput(attrs={'class': 'form-control','placeholder':'R$ 0,00'}),
            'hora_inicio':forms.TextInput(attrs={'class': 'form-control',}),
            'hora_final':forms.TextInput(attrs={'class': 'form-control',}),
            'status_pag':forms.CheckboxInput,
            'paciente':forms.Select(attrs={'class':'form-control'}),
            'profissional':forms.Select(attrs={'class':'form-control'}),
        }
