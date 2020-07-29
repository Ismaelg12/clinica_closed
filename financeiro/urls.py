from django.urls import path
from financeiro import views

urlpatterns = [
	path('contas/',views.conta_receber,name='conta_receber'),
	path('financeiro/',views.financeiro_dashboard,name='financeiro_dashboard'),
	path('contas/pagar/',views.contas_pagar,name='contas_a_pagar'),
	path('adicionar/contareceber/',views.adicionar_conta,name='add_conta'),
	path('sobre/contareceber/<int:pk>/',views.conta_detalhe,name='conta_detalhes'),
	path('efetuar/pagamento/<int:pk>/',views.efetuar_pagamento,name='fazer_pagamento'),
	#Contas a pagar
	path('efetuar/pag_realizado/',views.PagRealizadoPDF.as_view(),name='pag_realizado'),
	#efetua pagamento com geração de pdf
	path('recibos/',views.recibos,name='recibos'),
	#Faturados
	path('faturadas/',views.faturadas,name='faturadas'),
	#Faturamento
	path('faturamento/',views.faturamento,name='faturamento'),
	path('enviar/faturamento/',views.enviar_faturamento,name='enviar_faturamento'),
	path('retorno/faturamento/',views.retorno_faturado,name='retorno_faturamento'),
	#lotes
	path('lotes',views.lotes,name="lista_lotes"),
	path('lote/<int:pk>/detalhe',views.lote_detalhe,name="lote_detalhe"),
	#PDFS
	#path('imprimir/pdf/', views.generate_pdf, name='imprimir_recibos'),
]