from django.contrib import admin
from controle_usuarios.models import Profissional


class ProfissionalAdmin(admin.ModelAdmin):
	list_display = ['nome','sobrenome','tipo','data_cadastro','ativo','area_atuacao'] 
admin.site.register(Profissional,ProfissionalAdmin)
