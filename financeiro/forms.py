from django import forms
from financeiro.models import *

class ContaReceberForm(forms.ModelForm):
    class Meta:
        model = ContaReceber
        fields = ['forma_pagamento','valor_pago_dinheiro','valor_pago_cartao','cartao_credito','receptor']
        widgets = {
            'forma_pagamento':forms.Select(attrs={'class':'selectpicker',
            'data-style':'select-with-transition','data-size':7}),
            'receptor':forms.Select(attrs={'class':'selectpicker',
            'data-style':'select-with-transition','data-size':7}),
            'valor_pago_dinheiro':forms.NumberInput(attrs={'class': 'form-control','placeholder':'R$ 0,00'}),
            'valor_pago_cartao':forms.NumberInput(attrs={'class': 'form-control','placeholder':'R$ 0,00'}),
            'cartao_credito':forms.Select(attrs={'class': 'selectpicker',
            'data-style':'select-with-transition','data-size':7}),
        }
    def __init__(self, *args, **kwargs):
        super(ContaReceberForm, self).__init__(*args, **kwargs)
        #se profissional/atendente logado ele seta o tipo de recepção do pagamento
        if Profissional.prof_objects.filter(tipo=2).exists():
            self.initial['receptor'] = 'PF'
        else:
            self.initial['receptor'] = 'RC'



class ContaPagarForm(forms.ModelForm):
    class Meta:
        model = ContaPagar
        fields = '__all__'
        widgets = {
            'descricao':forms.TextInput(attrs={'class': 'form-control'}),
            'vencimento':forms.DateInput(attrs={'class': 'form-control','placeholder':'dd/mm/aaaa','data-language': 'pt'}),
            'valor_total':forms.TextInput(attrs={'class': 'form-control','placeholder':'R$ 0,00'}),
            'n_parcela':forms.Select(attrs={'class':'form-control'}),
            'status_pag':forms.CheckboxInput,
            'conta_fixa':forms.NullBooleanSelect(attrs={'class':'form-control'}),
            'forma_pagamento':forms.Select(attrs={'class':'form-control'}),
            'observacao':forms.Textarea(attrs={'class':'form-control','rows':6}),
            'categoria':forms.Select(attrs={'class':'form-control'}),
        }
