from django.shortcuts import render
from financeiro.models import ContaReceber

def conta_receber(request):
	conta = ContaReceber.objects.all()
	return render(request,'contas_receber.html',{'contas':conta})