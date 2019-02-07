from django.shortcuts import render,redirect
from financeiro.models import ContaReceber,ContaPagar
from financeiro.forms import ContaPagarForm
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                          Crud de Contas a receber
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

def conta_receber(request):
	conta = ContaReceber.objects.all()
	return render(request,'contas_receber.html',{'contas':conta})

'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                          Crud de Contas a pagar
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

def contas_pagar(request):
	conta = ContaPagar.objects.all()
	return render(request,'contas_pagar/contas.html',{'contas':conta})

def adicionar_conta(request):
	form = ContaPagarForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('contas_a_pagar')
	return render(request,'contas_pagar/adicionar_conta.html',{'form':form})