from django import forms
from financeiro.models import *

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
            'observacao':forms.Textarea(attrs={'class':'form-control','rows':5}),
            'categoria':forms.Select(attrs={'class':'form-control'}),
            }
