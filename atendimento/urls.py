from django.urls import path
from atendimento import views
from atendimento.render_pdf import *

urlpatterns = [
	path('agendamentos/',views.agendamento,name='agendamentos'),
	path('adicionar/agendamento/',views.add_agendamento,name='add_agendamento'),
	path('atualizar/agendamento/<int:pk>/',views.update_agendamento,name='update_agendamento'),
	path('agendamento/detalhe/<int:pk>/',views.agendamento_detalhe,name='agendamento_detalhe'),
	path('cancelar/agendamento/<int:pk>/',views.cancel_agendamento,name='cancel_agendamento'),
	path('desmarcar/agendamento/<int:pk>/',views.desmarcar_agendamento,name='desmarcar_agendamento'),
	path('liberar/agendamento/<int:pk>/',views.liberar_agendamento,name='liberar_agendamento'),
	#############Atendimento#############
	path('atendimentos/',views.atendimentos,name='atendimentos'),
	path('adicionar/atendimento/<int:pk>/',views.atendimento_add,name='add_atendimento'),
	path('atualizar/atendimento/<int:pk>/',views.atendimento_update,name='update_atendimento'),
	path('atendimento/detalhe/<int:pk>/',views.atendimento_detalhe,name='detalhe_atendimento'),
	path('excluir/atendimento/<int:pk>/',views.excluir_atendimento,name='excluir_atendimento'),
	path('ajax/procedimentos/', views.load_procedimentos_guias, name='ajax_load_proced'),
	#############Guias#############
	path('guias',views.guias,name='guias'),
	path('adicionar/guia',views.adicionar_guia,name='add_guia'),
	path('atualizar/guia/<int:pk>/',views.update_guia,name='update_guia'),
	####PDF############
	path('render/pdf/<int:pk>/',Pdf.as_view()),
	path('historico/pdf/<int:pk>/',Historico_Pdf.as_view(),name='pdf_historico')
	
]