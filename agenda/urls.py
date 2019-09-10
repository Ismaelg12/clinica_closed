from django.urls import path
from agenda import views
from agenda.agenda_pdf import *

urlpatterns = [
	#####################AGENDA DO FULL CALENDAR#############################################
	path('agenda/',views.agenda,name='agenda'),
	path('adicionar/agenda/',views.add_agend_calendar,name='add_agend_calendar'),#agenda FullCalendar(Create)
	path('update/agendamento/<int:pk>/calendar/',views.update_agend_calendar,name='update_agendamento'),
	path('deletar/agendamento/calendar',views.remove_agend_calendar,name='remove_agend_calendar'),#agenda fullCalendar(Remove)
	path('criar/paciente/',views.adicionar_paciente_calendar,name='adicionar_paciente_calendar'),#agenda fullCalendar(Remove)
	#path('ajax_calls/search/', views.autocompleteModel,name='autocomplete_search'),
	#########################################################################
	path('agendamentos/',views.agendamento,name='agendamentos'),
	path('adicionar/agendamento/',views.add_agendamento,name='add_agendamento'),
	path('atualizar/agendamento/<int:pk>/',views.update_agendamento,name='update_agendamento'),
	path('agendamento/detalhe/<int:pk>/',views.agendamento_detalhe,name='agendamento_detalhe'),
	path('cancelar/agendamento/<int:pk>/',views.cancel_agendamento,name='cancel_agendamento'),
	path('desmarcar/agendamento/<int:pk>/',views.desmarcar_agendamento,name='desmarcar_agendamento'),
	path('liberar/agendamento/<int:pk>/',views.liberar_agendamento,name='liberar_agendamento'),
	path('deletar/agendamento/<int:pk>/',views.deletar_agendamento,name='deletar_agendamento'),
	################################PDF#############################################
	path('render/pdf/<int:pk>/',Pdf.as_view()),
	path('historico/pdf/<int:pk>/',Historico_Pdf.as_view(),name='pdf_historico'),
	path('liberar/paciente/<int:pk>/',LiberarPacientePdf.as_view(),name='liberar_paciente_pdf'),
	path('imprimir/agendamento/<int:pk>/',ImprimirAgendamentos.as_view(),name='imprimir_agendamento_pdf'),
	
]