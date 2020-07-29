# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, Http404, FileResponse
from financeiro.models import ContaReceber,ContaPagar,Faturamento,ReciboPago,Lote
from core.models import Clinica
from controle_usuarios.models import Profissional
from financeiro.forms import ContaPagarForm,ContaReceberForm
from django.db.models import Count,Q,Sum
from datetime import datetime
from django.contrib import messages
#weasy print
from django.http import HttpResponse
from django.template.loader import render_to_string
#from weasyprint import HTML
import tempfile
import os
from django.views.generic import View

from financeiro.render_to_pdf import render_to_pdf
from django.template.loader import get_template
from io import BytesIO
from django.core.files import File

'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                          Crud de Contas a receber
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
def financeiro_dashboard(request):
    return render(request,'financeiro.html')


def conta_receber(request):
    pf = ""
    entradas = ""
    profissional_query = Profissional.prof_objects.filter(tipo=2)
    #variavel para distiguir atendimentos por profissional
    prof = ""
    #variaveis para saber o tipo de usuario logado no template
    profissional_logged = Profissional.prof_objects.filter(user=request.user,tipo=2)
    if profissional_logged.exists():
        prof = Profissional.prof_objects.get(user=request.user,tipo=2)
    else:
        pass
    
    if request.GET.get('date_ranger'):
        #se buscas
        date_range          = request.GET.get('date_ranger')
        start_date_string   = datetime.strptime(date_range.split(' / ')[0],'%d/%m/%Y').strftime('%Y-%m-%d')
        end_date_string     = datetime.strptime(date_range.split(' / ')[1],'%d/%m/%Y').strftime('%Y-%m-%d')
        profissional_search = request.GET.get('profissional')
        forma_pagamento     = request.GET.get('forma_pagamento')
        paciente            = request.GET.get('paciente')
        if prof:
            #se profissional estiver logado ele exibe a busca conforme ele
            conta = ContaReceber.objects.select_related('paciente','profissional').filter(
                data__range=(start_date_string,end_date_string),profissional_id=prof.id,paciente__nome__icontains=paciente,forma_pagamento=forma_pagamento).order_by('-data')
            #reatribui o valor do contexto com o novo valor
            contas     = Paginator(conta,25).get_page(request.GET.get('page'))
        else:
            #se admin estiver logado
            conta = ContaReceber.objects.select_related('paciente','profissional').filter(
                data__range=(start_date_string,end_date_string),
                profissional__nome__icontains=profissional_search,paciente__nome__icontains=paciente,forma_pagamento=forma_pagamento
               ).order_by('-data')
            #reatribui o valor do contexto com o novo valor
            contas     = Paginator(conta,25).get_page(request.GET.get('page'))
    else:
        #exibe todos os atendimentos quando abrir a pagina conforme o tipo de user logado
        if prof:
            conta      = ContaReceber.objects.select_related('paciente','profissional').filter(
                profissional_id=prof.id).order_by('-data')
            #lista de contas a receber
            contas     = Paginator(conta,25).get_page(request.GET.get('page'))
        else:
            conta      = ContaReceber.objects.select_related('paciente','profissional').order_by('-data')
            #lista de contas a receber
            contas     = Paginator(conta,25).get_page(request.GET.get('page'))
    valor_total_especie = conta.aggregate(
            total=Sum('valor_total'),
            especie=Sum('valor_total_pago'),
            cartao=Sum('valor_pago_cartao'),
        )
    if valor_total_especie['cartao'] != None and  valor_total_especie['especie'] != None:
        entradas = valor_total_especie['cartao'] + valor_total_especie['especie']
    context = {
        'pf':profissional_query,
        'lista_dados':contas,
        'valor':valor_total_especie,
        'profissional_logado':pf,
        'entradas':entradas

    }
    return render(request,'contas_receber/contas_receber.html',context)


def efetuar_pagamento(request,pk):
    conta             = get_object_or_404(ContaReceber,pk=pk)
    form              = ContaReceberForm(request.POST or None,instance=conta)
    forma_pagamento   = request.POST.get('forma_pagamento')
    valor_pago        = request.POST.get('valor_pago_dinheiro')
    valor_pago_cartao = request.POST.get('valor_pago_cartao')
    desconto          = request.POST.get('desconto')
    ##tratar excessao admin
    if form.is_valid():
        if (forma_pagamento == 'ES'):
            if float(valor_pago)  >= float(conta.valor_total) :
                print('valor total pago ',conta.valor_total, valor_pago)
                conta.valor_total_pago = float(conta.valor_total) - float(desconto)     
                conta.status = 'PG'
                conta.recebido_por= Profissional.prof_objects.get(user=request.user).nome
                conta.save()
                #especie multiplica pelo desconto
        elif (forma_pagamento == 'CD' or forma_pagamento == 'VS'  or 
                forma_pagamento == 'MC'  or forma_pagamento == 'AE'  
                or forma_pagamento == 'CS' or forma_pagamento == 'HP' or forma_pagamento == 'EO'):
            if float(valor_pago_cartao)  >= float(conta.valor_total) :
                print('valor total pago ',conta.valor_total, valor_pago_cartao)
                conta.valor_total_pago = valor_pago_cartao  
                conta.status = 'PG'
                conta.recebido_por=  Profissional.prof_objects.get(user=request.user).nome
                conta.save()
        elif (forma_pagamento == 'EC'):
            total = float(valor_pago_cartao) + float(valor_pago)
            print('valor',total)
            conta.valor_total_pago = total

            if  total >=float(conta.valor_total):
                conta.status = 'PG'
                conta.recebido_por= Profissional.prof_objects.get(user=request.user).nome
                conta.save()
        messages.success(request,
         "$ Pagamento feito com sucesso :)")        
        return redirect('conta_receber')
    return render(request,'contas_receber/efetuar_pagamento.html',{'form':form,'conta':conta})


def conta_detalhe(request,pk):
    conta             = get_object_or_404(ContaReceber,pk=pk)
    return render(request,'contas_receber/conta_detalhes.html',{'conta':conta})


'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                          Crud de Contas a pagar
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

def contas_pagar(request):
    #variavel para distiguir atendimentos por profissional
    prof = ""
    #variaveis para saber o tipo de usuario logado no template
    pf = Profissional.prof_objects.filter(user=request.user,tipo=2)
    if pf.exists():
        prof = Profissional.prof_objects.get(user=request.user,tipo=2)
    else:
        pass
    
    if request.GET.get('date_ranger'):
        #se buscas
        date_range          = request.GET.get('date_ranger')
        start_date_string   = datetime.strptime(date_range.split(' / ')[0],'%d/%m/%Y').strftime('%Y-%m-%d')
        end_date_string     = datetime.strptime(date_range.split(' / ')[1],'%d/%m/%Y').strftime('%Y-%m-%d')
        profissional_search = request.GET.get('profissional')
        forma_pagamento     = request.GET.get('forma_pagamento')
        paciente            = request.GET.get('paciente')
        if prof:
            #se profissional estiver logado ele exibe a busca conforme ele
            conta = ContaPagar.objects.select_related('paciente','profissional').filter(
                data__range=(start_date_string,end_date_string),
                status_pag=False,profissional_id=prof.id).order_by('-data')
            #reatribui o valor do contexto com o novo valor
            contas     = Paginator(conta,25).get_page(request.GET.get('page'))
        else:
            #se admin estiver logado
            conta = ContaPagar.objects.select_related('paciente','profissional').filter(
                data__range=(start_date_string,end_date_string),
                profissional__nome__icontains=profissional_search,
                status_pag=False).order_by('-data')
            #reatribui o valor do contexto com o novo valor
            contas     = Paginator(conta,25).get_page(request.GET.get('page'))
    else:
        #exibe todos os atendimentos quando abrir a pagina conforme o tipo de user logado
        if prof:
            conta      = ContaPagar.objects.select_related('paciente','profissional').filter(
                profissional_id=prof.id,status_pag=False).order_by('-data')
            #lista de contas a receber
            contas     = Paginator(conta,25).get_page(request.GET.get('page'))
        else:
            conta      = ContaPagar.objects.select_related('paciente','profissional').filter(
                status_pag=False).order_by('-data')
            #lista de contas a receber
            contas     = Paginator(conta,25).get_page(request.GET.get('page'))

    return render(request,'contas_pagar/contas.html',{'lista_dados':contas})


def recibos(request):
    #variavel para distiguir atendimentos por profissional
    prof = ""
    #variaveis para saber o tipo de usuario logado no template
    pf = Profissional.prof_objects.filter(user=request.user,tipo=2)
    if pf.exists():
        prof = Profissional.prof_objects.get(user=request.user,tipo=2)
    else:
        pass
    
    if request.GET.get('date_ranger'):
        #se buscas
        date_range          = request.GET.get('date_ranger')
        start_date_string   = datetime.strptime(date_range.split(' / ')[0],'%d/%m/%Y').strftime('%Y-%m-%d')
        end_date_string     = datetime.strptime(date_range.split(' / ')[1],'%d/%m/%Y').strftime('%Y-%m-%d')
        profissional_search = request.GET.get('profissional')
        forma_pagamento     = request.GET.get('forma_pagamento')
        paciente            = request.GET.get('paciente')
        if prof:
            #se profissional estiver logado ele exibe a busca conforme ele
            conta = ReciboPago.objects.filter(data_upload__date__range=(
                start_date_string,end_date_string),profissional_id=prof.id).order_by('-data_upload')
            #reatribui o valor do contexto com o novo valor
            contas     = Paginator(conta,25).get_page(request.GET.get('page'))
        else:
            #se admin estiver logado
            conta = ReciboPago.objects.filter(data_upload__date__range=(
                start_date_string,end_date_string), profissional__nome__icontains=profissional_search,
            ).order_by('-data_upload')
            #reatribui o valor do contexto com o novo valor
            contas     = Paginator(conta,25).get_page(request.GET.get('page'))
    else:
        #exibe todos os atendimentos quando abrir a pagina conforme o tipo de user logado
        if prof:
            conta      = ReciboPago.objects.select_related('profissional').filter(
                profissional_id=prof.id).order_by('-data_upload')
            #lista de recibos pagos profissional
            contas     = Paginator(conta,25).get_page(request.GET.get('page'))
        else:
            conta      = ReciboPago.objects.select_related('profissional').order_by('-data_upload')
            #lista de recibos pagos admin
            contas     = Paginator(conta,25).get_page(request.GET.get('page'))

    return render(request,'contas_pagar/recibos_pagos.html',{'lista_dados':contas})


#imprimir recibos e realizar pagamentos    
class PagRealizadoPDF(View):
    #https://www.codingforentrepreneurs.com/blog/save-a-auto-generated-pdf-file-django-model
    #https://www.codingforentrepreneurs.com/blog/html-template-to-pdf-in-django/
    #efetua pagamento com geração de pdf com o nome do profissional
    def get(self, request, *args, **kwargs):
        clinica = Clinica.objects.get(pk=1)
        template = get_template('relatorios.html')
        valor_total = 0
        if request.method == 'GET':
            contas = ContaPagar.objects.filter(id__in=request.GET.getlist('checkbox'))
            for c in contas:
                c.status_pag = True
                valor_total += float(c.valor_total)
                c.save()
        context = {
            'recibos': contas,
            'clinica':clinica,
            'profissional': contas[0].profissional.nome,
            'valor_total':valor_total
            #'area_atuacao': contas[0].profissional.area_atuacao,
        }
        html = template.render(context)
        pdf  = render_to_pdf('relatorios.html', context)
        obj  = ReciboPago.objects.create(documento='documento', 
            profissional_id=contas[0].profissional.id)
        if pdf:
            filename = "%s_recibo.pdf" %(contas[0].profissional.nome)
            obj.documento.save(filename, File(BytesIO(pdf.content)))
            response = HttpResponse(pdf, content_type='application/pdf')
            content  = "attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Pdf Não Existente")


def adicionar_conta(request):
    form = ContaPagarForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('contas_a_pagar')
    return render(request,'contas_pagar/adicionar_conta.html',{'form':form})

'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                          Crud de Faturamento
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

def faturamento(request):
    if Profissional.prof_objects.filter(user=request.user,tipo=2).exists():
        pf    = Profissional.prof_objects.get(user=request.user,tipo=2)
        faturado = Faturamento.objects.filter(profissional_id=pf.id,status_pag=False).order_by('atendimento__data')
        conta = Paginator(faturado,50).get_page(request.GET.get('page'))
    else:
        faturado = Faturamento.objects.select_related(
            'paciente','atendimento','profissional').filter(status_pag=False).order_by('atendimento__data')
        conta = Paginator(faturado,50).get_page(request.GET.get('page'))
    return render(request,'contas_convenio/faturamento_convenio.html',{'lista_dados':conta})

#Contas a Receber de Procedimento Convenio
def faturadas(request):
    aggregate = ''
    if Profissional.prof_objects.filter(user=request.user,tipo=2).exists():
        pf    = Profissional.prof_objects.get(user=request.user,tipo=2)
        faturado = Faturamento.objects.filter(profissional_id=pf.id,status_pag=True)
    else:
        faturado = Faturamento.objects.select_related(
            'paciente','atendimento','profissional').filter(status_pag=True)
        # aggregate = Faturamento.objects.values('data_guia',
        # 'numero_guia','paciente__nome','profissional__nome').annotate(Count('id'),
        # Sum('valor_unitario')).order_by().filter(id__count__gt=0) 
    return render(request,'contas_convenio/faturadas.html',{'lista_dados':faturado})

def enviar_faturamento(request):
    if request.method == 'GET':
        faturamento = Faturamento.objects.filter(id__in=request.GET.getlist('checkbox'))
        lot = Lote.objects.create()
        lot.save()
        print('lote',lot.id)
        for f in faturamento:
            f.lote = lot
            f.status_pag = True
            f.save()
        messages.success(request,
         "Lote Criado com Sucesso :)")
        return redirect('faturamento')
    return render(request,'contas_convenio/faturamento_convenio.html')

#listagem de lotes
def lotes(request):
    lotes = Lote.objects.all()
    # departments = Lote.objects.all()
    # num_products = 0
    # for dept in departments : 
    # # Get the number of reviewed products for a given range and department
    #     num_products = dept.faturamento_set.all().count()
    #     print(num_products)
    #depts = Lote.objects.all().annotate(num_products=Count('faturamento',))
    return render(request,'lotes/lista_lotes.html',{'lotes':lotes})

def lote_detalhe(request,pk):
    lote = get_object_or_404(Lote,pk=pk)
    #faturamentos agregados
    lote_aggregate = Faturamento.objects.values('data_guia',
        'numero_guia','paciente__nome','profissional__nome',
        'procedimento','valor_unitario').annotate(Count('id'),
        Sum('valor_unitario')).order_by().filter(id__count__gt=0,lote=lote) 
    return render(request,'lotes/lote_detalhe.html',{'lote':lote,'lote_aggregate':lote_aggregate})


def retorno_faturado(request):
    if request.method == 'GET':
        faturada     = Faturamento.objects.filter(id__in=request.GET.getlist('faturada'))
        nao_faturado = Faturamento.objects.filter(id__in=request.GET.getlist('nFat'))
        print(faturada)
        print(nao_faturado)
        for f in faturada:
            f.status_fat = True
            f.save()
        for f in nao_faturado:
            f.status_nf = True
            f.save()
        return redirect('faturadas')
    return render(request,'contas_convenio/faturamento_convenio.html')
    
"""Generate pdf."""
"""
def generate_pdf(request):
    # https://dev.to/djangotricks/how-to-create-pdf-documents-with-django-in-2019-5gb9
    # https://www.bedjango.com/blog/how-generate-pdf-django-weasyprint/
    # Model data
    recibos = ContaPagar.objects.filter(status_pag=True)

    # Rendered
    html_string = render_to_string('relatorios.html', {'recibos': recibos})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=lista_contas.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())
    return response
"""