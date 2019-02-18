from django.shortcuts import render,redirect,get_object_or_404
from financeiro.models import ContaReceber,ContaPagar
from controle_usuarios.models import Profissional
from financeiro.forms import ContaPagarForm,ContaPagamentoForm
from django.db.models import Count,Q,Sum
from datetime import datetime
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                          Crud de Contas a receber
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

def conta_receber(request):
	profissional = Profissional.objects.filter(tipo=2)
	if request.GET.get('date_ranger'):
		date_range          = request.GET.get('date_ranger')
		start_date_string   = datetime.strptime(date_range.split(' / ')[0],'%d/%m/%Y').strftime('%Y-%m-%d')
		end_date_string     = datetime.strptime(date_range.split(' / ')[1],'%d/%m/%Y').strftime('%Y-%m-%d')
		profissional_search = request.GET.get('profissional')
		status              = request.GET.get('status')
		#cobnvenio            = request.GET.get('paciente')
		if status != None:
			conta = ContaReceber.objects.filter(data__range=(start_date_string,end_date_string),status=status)
		else:
			conta = ContaReceber.objects.filter(data__range=(start_date_string,end_date_string))
	else:
		conta = ContaReceber.objects.all().order_by('-data')

	valor_total_especie = conta.aggregate(
			total=Sum('valor_total'),
			especie=Sum('valor_pago_dinheiro'),
			cartao=Sum('valor_pago_cartao'),
		)
	context = {
		'pf':profissional,
		'contas':conta,
		'valor':valor_total_especie,
	}
	return render(request,'contas_receber.html',context)

def efetuar_pagamento(request,pk):
	conta = get_object_or_404(ContaReceber,pk=pk)
	form  = ContaPagamentoForm(request.POST or None,instance=conta)
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