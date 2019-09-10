from django.contrib import admin
from agenda.models import Agendamento
# Register your models here.

class AgendamentoAdmin(admin.ModelAdmin):
	list_display  = ('data','paciente','profissional',
		'status', 'convenio','hora_inicio', 'hora_fim')
	list_filter   = ('data','profissional','status')
	search_fields = ('data','paciente__nome')

admin.site.register(Agendamento, AgendamentoAdmin)
