from django import forms
from django.forms import ModelForm
from pacientes.models import *

class PacienteForm(forms.ModelForm):
	class Meta:
          model   = Paciente
          fields  = '__all__'
          widgets = {
          'nome'           : forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
          'email'          : forms.EmailInput(attrs={'class': 'form-control input-rounded'}),
          'data_nascimento': forms.DateInput(attrs={'class': 'form-control','required': 'true'}),
          'sexo'           : forms.Select(attrs={'class': 'form-control','required': 'true'}),
          'raca'           : forms.Select(attrs={'class':'selectpicker','data-style':'select-with-transition','data-size':5,'required': 'true'}),
          'cpf'            : forms.TextInput(attrs={'class': 'form-control'}),
          'rg'             : forms.TextInput(attrs={'class': 'form-control'}),
          'estado_civil'   : forms.Select(attrs={'class':'selectpicker','data-style':'select-with-transition','data-size':5,'required': 'true'}),
          'profissao'      : forms.TextInput(attrs={'class': 'form-control'}),
          'rua'            : forms.TextInput(attrs={'class': 'form-control','required': 'true'}),
          'bairro'         : forms.TextInput(attrs={'class': 'form-control','required': 'true'}),
          'cidade'         : forms.TextInput(attrs={'class': 'form-control','required': 'true'}),
          'cep'            : forms.TextInput(attrs={'class': 'form-control'}),
          'complemento'    : forms.TextInput(attrs={'class': 'form-control'}),
          'uf'             : forms.Select(attrs={'class':'selectpicker','data-style':'select-with-transition','data-size':7,'data-live-search':'true'}),
          'telefone'       : forms.TextInput(attrs={'class': 'form-control'}),
          'convenio'       : forms.Select(attrs={'class':'selectpicker','data-style':'select-with-transition','data-size':7,'data-live-search':'true','required': 'true'}),
          'num_convenio'   : forms.TextInput(attrs={'class': 'form-control'}),
          'num_convenio'   : forms.TextInput(attrs={'class': 'form-control'}),
          'num_convenio'   : forms.TextInput(attrs={'class': 'form-control'}),
          'responsavel'    : forms.TextInput(attrs={'class': 'form-control'}),
          'observacao'     : forms.Textarea(attrs={'class': 'form-control'}),
      }
