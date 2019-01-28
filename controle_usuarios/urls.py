from django.urls import path
from controle_usuarios import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('login',auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
	path('bemvindo/',views.login_success,name="login_success"),
	path('sair',auth_views.LogoutView.as_view(), name='logout'),
	path('atualizar/profissional/<int:pk>/',views.update_profissional,name="atualizar_profissional"),
	path('profissional/detalhe/<int:pk>/detalhe',views.profissional_detalhe,name="profissional_detalhe"),
	path('deletar/profissional/<int:pk>/',views.excluir_profissional,name="deletar_profissional"),
	path('profissionais',views.profissionais,name="profissionais"),
	path('adicionar/profissional/',views.add_profissional,name='cadastrar_profissional')
]