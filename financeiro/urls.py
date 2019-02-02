from django.urls import path
from financeiro import views

urlpatterns = [
	path('contas',views.conta_receber,name='conta_receber')
]