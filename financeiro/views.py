from django.shortcuts import render,redirect,get_object_or_404
from financeiro.models import ContaReceber,ContaPagar
from financeiro.forms import ContaPagarForm,ContaPagamentoForm
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                          Crud de Contas a receber
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

def conta_receber(request):
	conta = ContaReceber.objects.all()
	return render(request,'contas_receber.html',{'contas':conta})

def efetuar_pagamento(request,pk):
	conta = get_object_or_404(ContaReceber,pk=pk)
	form = ContaPagamentoForm(request.POST or None,instance=conta)
	if form.is_valid():
		conta.status = 'PG'
		conta.save()
		form.save()
		return redirect('/historico/paciente/'+ str(int(conta.paciente.id)))
	return render(request,'contas_receber/efetuar_pagamento.html',{'form':form,'conta':conta})
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