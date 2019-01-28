from django.contrib import admin
from atendimento.models import Agendamento,Atendimento

class AgendamentoAdmin(admin.ModelAdmin):
	list_display = ('data','paciente','profissional','liberado')

admin.site.register(Agendamento,AgendamentoAdmin)
admin.site.register(Atendimento)