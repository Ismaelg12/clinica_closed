from django.urls import path
from financeiro import views

urlpatterns = [
	path('contas/',views.conta_receber,name='conta_receber'),
	path('contas/pagar/',views.contas_pagar,name='contas_a_pagar'),
	path('adicionar/contareceber/',views.adicionar_conta,name='add_conta'),
	path('efetuar/pagamento/<int:pk>/',views.efetuar_pagamento,name='fazer_pagamento')
]