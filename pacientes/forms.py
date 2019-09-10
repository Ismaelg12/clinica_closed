from django import forms
from django.forms import ModelForm
from pacientes.models import *
from django.core.exceptions import ValidationError
from .models import Profissional

class PacienteForm(forms.ModelForm):
	profissional = forms.ModelMultipleChoiceField(
		queryset = Profissional.objects.all(),
		widget   =   forms.SelectMultiple(attrs={'class':'selectpicker',
		'data-style':'select-with-transition','data-size':7,
		'data-live-search':'true','multiple':'multiple','title':'escolha os profissionais'})
	)

	class Meta:
		model   = Paciente
		fields  = '__all__'
		widgets = {
			'nome'           : forms.TextInput(attrs={'class': 'form-control','required': 'true' }),
			'email'          : forms.EmailInput(attrs={'class': 'form-control input-rounded'}),
			#'profissional'   : forms.Select(attrs={'class':'selectpicker',
			#	'multiple':'multiple'}),
			'data_nascimento': forms.DateInput(attrs={'class': 'form-control'}),
			'sexo'           : forms.Select(attrs={'class': 'form-control'}),
			'raca'           : forms.Select(attrs={'class':'selectpicker',
				'data-style':'select-with-transition','data-size':5}),
			'cpf'            : forms.TextInput(attrs={'class': 'form-control'}),
			'rg'             : forms.TextInput(attrs={'class': 'form-control'}),
			'estado_civil'   : forms.Select(attrs={'class':'selectpicker',
				'data-style':'select-with-transition','data-size':5}),
			'profissao'      : forms.TextInput(attrs={'class': 'form-control'}),
			'rua'            : forms.TextInput(attrs={'class': 'form-control'}),
			'bairro'         : forms.TextInput(attrs={'class': 'form-control'}),
			'cidade'         : forms.TextInput(attrs={'class': 'form-control'}),
			'cep'            : forms.TextInput(attrs={'class': 'form-control'}),
			'complemento'    : forms.TextInput(attrs={'class': 'form-control'}),
			'uf'             : forms.Select(attrs={'class':'selectpicker',
				'data-style':'select-with-transition','data-size':7,'data-live-search':'true'}),
			'telefone'       : forms.TextInput(attrs={'class': 'form-control','required': 'true'}),
			'telefone_fixo'  : forms.TextInput(attrs={'class': 'form-control'}),
			'convenio'       : forms.Select(attrs={'class':'selectpicker',
				'data-style':'select-with-transition','data-size':7,
				'data-live-search':'true','required': 'true','onchange':'showDiv(this)','id':'id_convenio',}),
			'num_convenio'   : forms.TextInput(attrs={'class': 'form-control'}),
			'pai'            : forms.TextInput(attrs={'class': 'form-control'}),
			'mae'            : forms.TextInput(attrs={'class': 'form-control'}),
			'validade_carteira': forms.DateInput(attrs={'class': 'form-control'}),
			'observacao'     : forms.Textarea(attrs={'class': 'form-control'}),
		}


	def clean_cpf(self):
		if self.cleaned_data['cpf'] == "":
			return None
		else:
			return self.cleaned_data['cpf']
	
	#valida se tem registros duplicados no banco
	def clean(self):
		nome = self.cleaned_data['nome']
		data_nascimento = self.cleaned_data['data_nascimento']
		if not data_nascimento:
			raise ValidationError('Preencha a Data de Nasciemnto.')
		if Paciente.objects.filter(nome__iexact=nome,data_nascimento__iexact=data_nascimento,id=self.instance.id).exists():
			#raise ValidationError('Atualizando dados')
			pass
		elif Paciente.objects.filter(nome__iexact=nome,data_nascimento__iexact=data_nascimento).exists():
			raise ValidationError('Paciente Já existe na base da dados!')
		return None
	