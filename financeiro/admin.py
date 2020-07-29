from django.contrib import admin
from financeiro.models import ContaReceber,ContaPagar,Categoria,Faturamento,ReciboPago,Lote

class ContaAdmin(admin.ModelAdmin):
	list_display = (
		'data','agendamento','paciente','valor_total',
		'forma_pagamento','profissional','recebido_por'
	)
	list_filter = ['data']
	search_fields  = ['paciente__nome','profissional__nome']
	list_select_related = ['agendamento','paciente','profissional']

class ReciboAdmin(admin.ModelAdmin):
	list_display = (
		'data_upload','profissional'
	)
	list_filter = ['data_upload']
	search_fields  = ['data_upload','profissional__nome']

class ContaPagarAdmin(admin.ModelAdmin):
	list_display = (
		'data','paciente','valor_total',
		'profissional','status_pag'
	)
	list_filter = ['data','status_pag']
	search_fields  = ['paciente__nome','profissional__nome','status_pag']

class FaturamentoAdmin(admin.ModelAdmin):
	list_display = ['paciente','lote']
	search_fields  = ['paciente__nome']

class LoteAdmin(admin.ModelAdmin):
	list_display = (
		'criado_em',
	)
admin.site.register(ContaReceber,ContaAdmin)
admin.site.register(ContaPagar,ContaPagarAdmin)
admin.site.register(Faturamento,FaturamentoAdmin)
admin.site.register(ReciboPago,ReciboAdmin)
admin.site.register(Lote,LoteAdmin)