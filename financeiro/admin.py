from django.contrib import admin
from financeiro.models import ContaReceber,ContaPagar,Categoria

class ContaAdmin(admin.ModelAdmin):
	list_display = (
		'data','agendamento','paciente','valor_total',
		'forma_pagamento','convenio','receptor'
	)
admin.site.register(ContaReceber,ContaAdmin)
admin.site.register(ContaPagar)
admin.site.register(Categoria)