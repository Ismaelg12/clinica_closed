from django.contrib import admin
from controle_usuarios.models import Profissional,Perfil


class ProfissionalAdmin(admin.ModelAdmin):
	list_display = ['user','nome','sobrenome','tipo','data_cadastro','email', 'ativo'] 
	search_fields = ['nome']
admin.site.register(Profissional,ProfissionalAdmin)
admin.site.register(Perfil)
