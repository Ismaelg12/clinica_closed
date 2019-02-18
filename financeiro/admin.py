from django.contrib import admin
from financeiro.models import ContaReceber,ContaPagar,Categoria

class ContaAdmin(admin.ModelAdmin):
	list_display = ('data','atendimento','paciente','valor_total','forma_pagamento')
admin.site.register(ContaReceber,ContaAdmin)
admin.site.register(ContaPagar)
admin.site.register(Categoria)