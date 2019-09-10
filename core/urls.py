from django.urls import path
from core import views
from django.views.generic.base import TemplateView

urlpatterns = [
	path('dashboard/',views.DashboardView.as_view(),name='home'),
	path('aniversariantes/',views.aniversarios,name='aniversario'),
	path('vagas/',views.vagas,name='vagas'),
	######################CONVENIOS############################################
	path('convenios/',views.ConvenioListView.as_view(),name='convenios'),
	path('adicionar/convenio/',views.ConvenioCreateView.as_view(),name='add_convenio'),
	path('convenio/detalhe/<int:pk>/',views.ConvenioDetailView.as_view(),name='convenio_detalhe'),
	path('atualizar/convenio/<int:pk>/',views.ConvenioUpdateView.as_view(),name='update_convenio'),
	path('deletar/convenio/<int:pk>/',views.ConvenioDeleteView,name='deletar_convenio'),
	#######################SALAS##################################################
	path('salas/',views.SalaListView.as_view(),name='salas'),
	path('adicionar/sala/',views.SalaCreateView.as_view(),name='add_sala'),
	path('atualizar/sala/<int:pk>/',views.SalaUpdateView.as_view(),name='update_sala'),
	path('deletar/sala/<int:pk>/',views.SalaDeleteView.as_view(),name='deletar_sala'),
	######################PROCEDIMENTOS############################################
	path('procedimentos/',views.ProcedListView.as_view(),name='procedimentos'),
	path('adicionar/procedimento/',views.ProcedCreateView.as_view(),name='add_procedimento'),
	path('atualizar/procedimento/<int:pk>/',views.ProcedUpdateView.as_view(),name='update_procedimento'),
	path('deletar/procedimento/<int:pk>/',views.ProcedDeleteView,name='deletar_procedimento'),
	######################LISTA DE ESPERA############################################
	path('lista_espera/',views.EsperaListView.as_view(),name='lista_espera'),
	path('ajax/profissionais/', views.load_profissional, name='ajax_load_profissionais'),
	path('adicionar/lista_espera/',views.EsperaCreateView.as_view(),name='add_lista'),
	path('atualizar/lista_espera/<int:pk>/',views.EsperaUpdateView.as_view(),name='update_lista_espera'),
	path('lista_espera/<int:pk>/migrar_paciente/',views.migrar_paciente,name='migrar_paciente'),
	path('lista_espera/<int:pk>/detalhe/',views.EsperaDetailView.as_view(),name='lista_espera_detalhe'),
	path('deletar/lista_espera/<int:pk>/',views.EsperaDeleteView.as_view(),name='deletar_lista_espera'),
	####################################ACESSO NEGADO##########################################
	path('acesso/negado/',TemplateView.as_view(template_name="erros/403.html"),name='erro_403'),
]