from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from controle_usuarios.models import Profissional

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )
        
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        
class ProfissinalForm(forms.ModelForm):
    class Meta:
        model   = Profissional
        exclude = ['user']
        fields  = '__all__'
        widgets = {
            'user'            : forms.Select(attrs={'class': 'form-control '}),
            'nome'            : forms.TextInput(attrs={'class': 'form-control'}),
            'sobrenome'       : forms.TextInput(attrs={'class': 'form-control'}),
            'email'           : forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone'        : forms.TextInput(attrs={'class': 'form-control'}),
            'registro'        : forms.TextInput(attrs={'class': 'form-control'}),
            'cpf'             : forms.TextInput(attrs={'class': 'form-control',}),
            'area_atuacao'    : forms.Select(attrs={'class': 'form-control',}),
            'data_nascimento' : forms.DateInput(attrs={'class': 'form-control',}),
            'quantidade_atend': forms.Select(attrs={'class': 'form-control',}),
            'tipo'            : forms.Select(attrs={'class': 'form-control','disabled':'disabled'}),
		}