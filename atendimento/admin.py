from django.contrib import admin
from atendimento.models import *

class GuiaAdmin(admin.ModelAdmin):
	list_display = ('numero','validade','paciente','quantidade',
		'atualizado_em','ativo')
	search_fields = ('paciente__nome',)

class AtendimentoAdmin(admin.ModelAdmin):
	list_display = ('tipo','data','paciente','hora_inicio','hora_fim','procedimento',
'criado_em')
	search_fields = ('paciente__nome',)


class EvolucaoAdmin(admin.ModelAdmin):
	list_display = ('paciente_nome','data_atendimento','procedimento_atendimento','convenio_atendimento')
	def paciente_nome(self, instance):
		return instance.atendimento.paciente
	def data_atendimento(self, instance):
		return instance.atendimento.data
	def procedimento_atendimento(self, instance):
		return instance.atendimento.procedimento
	def convenio_atendimento(self, instance):
		return instance.atendimento.convenio

admin.site.register(Atendimento,AtendimentoAdmin)
admin.site.register(Evolucao,EvolucaoAdmin)
admin.site.register(TerapiaOcupacional)
admin.site.register(Guia,GuiaAdmin)
admin.site.register(Psiquiatria)
admin.site.register(Fisioterapeuta)
admin.site.register(Anaminese_adulto)
admin.site.register(Anaminese_crianca)
admin.site.register(Uroginecologia)
admin.site.register(Neurologia)