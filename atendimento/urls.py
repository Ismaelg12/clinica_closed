from django.urls import path
from atendimento import views
from atendimento.render_pdf import *

urlpatterns = [

	#############Atendimento#############
	path('atendimentos/',views.atendimentos,name='atendimentos'),
	path('adicionar/atendimento/<int:pk>/',views.atendimento_add,name='add_atendimento'),
	path('atualizar/atendimento/<int:pk>/',views.atendimento_update,name='update_atendimento'),
	#path('atendimento/detalhe/<int:pk>/',views.atendimento_detalhe,name='detalhe_atendimento'),
	path('excluir/atendimento/<int:pk>/',views.excluir_atendimento,name='excluir_atendimento'),
	path('ajax/procedimentos/', views.load_procedimentos_guias, name='ajax_load_proced'),
	#############Guias#############
	path('guias',views.guias,name='guias'),
	path('adicionar/guia',views.adicionar_guia,name='add_guia'),
	path('atualizar/guia/<int:pk>/',views.update_guia,name='update_guia'),
	path('finalizar/guia/<int:pk>/',views.finalizar_guia,name='finalizar_guia'),
	path('validar/guia/<int:pk>/',views.validar_guia,name='validar_guia'),
	path('excluir/guia/<int:pk>/',views.excluir_guia,name='excluir_guia'),
]