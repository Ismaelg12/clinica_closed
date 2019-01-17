from django.urls import path
from pacientes import views

urlpatterns = [
	path('pacientes/',views.PacienteListView.as_view(),name='lista_pacientes'),
	path('adicionar/paciente',views.PacienteCreateView.as_view(),name='add_paciente'),
	path('atualizar/paciente/<int:pk>',views.PacienteUpdateView.as_view(),name='update_paciente'),
	path('detalhe/paciente/<int:pk>',views.PacienteDetailView.as_view(),name='paciente_detalhe'),
	path('deletar/paciente/<int:pk>',views.PacienteDeleteView,name='delete_paciente'),
	path('historico/paciente/<int:pk>',views.paciente_historico,name='historico')
]


