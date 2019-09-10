from django.shortcuts import render,redirect,get_object_or_404
from financeiro.models import ContaReceber,ContaPagar
from controle_usuarios.models import Profissional
from financeiro.forms import ContaPagarForm,ContaReceberForm
from django.db.models import Count,Q,Sum
from datetime import datetime
from django.contrib import messages
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                          Crud de Contas a receber
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

def conta_receber(request):
	pf = ""
	profissional_query = Profissional.prof_objects.filter(tipo=2)
	if Profissional.prof_objects.filter(user=request.user,tipo=2).exists():
		pf = Profissional.prof_objects.get(user=request.user,tipo=2)
		if request.GET.get('date_ranger'):
			date_range          = request.GET.get('date_ranger')
			start_date_string   = datetime.strptime(date_range.split(' / ')[0],'%d/%m/%Y').strftime('%Y-%m-%d')
			end_date_string     = datetime.strptime(date_range.split(' / ')[1],'%d/%m/%Y').strftime('%Y-%m-%d')
			profissional_search = request.GET.get('profissional')
			status              = request.GET.get('status')
			convenio            = request.GET.get('convenio')
			paciente            = request.GET.get('paciente')
			print('querys',profissional_search,status,convenio,paciente)
			if status != None:
				conta = ContaReceber.objects.filter(data__range=(start_date_string,end_date_string),
					status=status,paciente__nome__icontains=paciente,
					profissional__nome__icontains=profissional_search,
					convenio__nome__icontains=convenio)
			else:
				conta = ContaReceber.objects.filter(data__range=(start_date_string,end_date_string),
					paciente__nome__icontains=paciente,
					profissional__nome__icontains=profissional_search,
					convenio__nome__icontains=convenio)
		else:
			conta = ContaReceber.objects.filter(profissional_id=pf.id).order_by('-data')
	else:
		conta = ContaReceber.objects.all().order_by('-data')
		
	valor_total_especie = conta.aggregate(
			total=Sum('valor_total'),
			especie=Sum('valor_pago_dinheiro'),
			cartao=Sum('valor_pago_cartao'),
		)
	context = {
		'pf':profissional_query,
		'contas':conta,
		'valor':valor_total_especie,
		'profissional_logado':pf,

	}
	return render(request,'contas_receber/contas_receber.html',context)


def efetuar_pagamento(request,pk):
	conta             = get_object_or_404(ContaReceber,pk=pk)
	form              = ContaReceberForm(request.POST or None,instance=conta)
	forma_pagamento   = request.POST.get('forma_pagamento')
	valor_pago        = request.POST.get('valor_pago_dinheiro')
	valor_pago_cartao = request.POST.get('valor_pago_cartao')
	if form.is_valid():
		if (forma_pagamento == 'DI' or forma_pagamento == 'CV' or 
			forma_pagamento == 'TB' or forma_pagamento == 'BB' or forma_pagamento == 'DC'):
			if float(valor_pago)  >= float(conta.valor_total) :
				print('valor total pago ',conta.valor_total, valor_pago)		
				conta.status = 'PG'
				conta.save()
			else:
				saldo = float(conta.valor_total) - float(valor_pago)
				conta.status = 'PC'
				conta.save()
				print('conta não paga toda e saldo que falta é ',saldo)
		elif (forma_pagamento == 'CC'):
			if float(valor_pago_cartao)  >= float(conta.valor_total) :
				print('valor total pago ',conta.valor_total, valor_pago_cartao)		
				conta.status = 'PG'
				conta.save()
			else:
				saldo = float(conta.valor_total) - float(valor_pago_cartao)
				conta.status = 'PC'
				conta.save()
				print('conta não paga toda e saldo que falta é ',saldo)
		elif (forma_pagamento == 'EC'):
			total = float(valor_pago_cartao) + float(valor_pago)
			print('valor',total)

			if  total >=float(conta.valor_total):
				conta.status = 'PG'
				conta.save()
			else:
				saldo = float(conta.valor_total) - total
				conta.status = 'PC'
				conta.save()
				print('conta não paga toda e saldo que falta é ',saldo)
		messages.success(request,
		 "$ Pagamento feito com sucesso :)")		
		return redirect('conta_receber')
	return render(request,'contas_receber/efetuar_pagamento.html',{'form':form,'conta':conta})
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                          Crud de Contas a pagar
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

def contas_pagar(request):
	if Profissional.prof_objects.filter(user=request.user,tipo=2).exists():
		pf    = Profissional.prof_objects.get(user=request.user,tipo=2)
		conta = ContaPagar.objects.filter(profissional_id=pf.id).order_by('-vencimento')
	else:
		conta = ContaPagar.objects.all().order_by('-vencimento')
	return render(request,'contas_pagar/contas.html',{'contas':conta})

def adicionar_conta(request):
	form = ContaPagarForm(request.POST or None)
	if form.is_valid():
		form.save()
		return redirect('contas_a_pagar')
	return render(request,'contas_pagar/adicionar_conta.html',{'form':form})