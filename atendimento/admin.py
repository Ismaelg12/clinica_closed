from django.contrib import admin
from atendimento.models import Agendamento,Atendimento,Guia

class AgendamentoAdmin(admin.ModelAdmin):
	list_display = ('data','paciente','profissional','liberado')

class GuiaAdmin(admin.ModelAdmin):
	list_display = ('numero','validade','paciente','quantidade')

admin.site.register(Agendamento,AgendamentoAdmin)
admin.site.register(Atendimento)
admin.site.register(Guia,GuiaAdmin)