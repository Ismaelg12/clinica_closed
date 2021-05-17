# -*- coding: utf-8 -*-
from django.utils import timezone
from agenda.forms import AgendaForm
import json
#import datetime
from datetime import date, datetime, timedelta
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from atendimento.forms import *
from atendimento.models import Atendimento,Guia,Evolucao
from agenda.models import Agendamento
from core.models import Sala,Convenio,Procedimento
from pacientes.models import Paciente
from controle_usuarios.models import Profissional
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from agenda.agenda_pdf import *
from django.db.models import ProtectedError
from django.forms import inlineformset_factory
from dateutil.relativedelta import relativedelta
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           Crud de Agenda FullCalendar
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

def add_agend_calendar(request):
    data_now  = request.POST.get('data', None)
    new_dates = datetime.strptime(data_now,'%d/%m/%Y')

    sessoes   = int(request.POST.get("sessoes", None))
    for i in range(0,sessoes):
        if i != 0:
            new_dates += relativedelta(days=7)
        new_agendamento                 = Agendamento()
        new_agendamento.data            = new_dates
        new_agendamento.hora_inicio     = request.POST.get('hora_inicio',None)
        new_agendamento.hora_fim        = request.POST.get('hora_fim',None)
        new_agendamento.paciente_id     = request.POST.get('paciente',None)
        new_agendamento.profissional_id = request.POST.get('profissional',None)
        new_agendamento.telefone        = request.POST.get('telefone', None)
        new_agendamento.observacao      = request.POST.get('observacao',None)
        new_agendamento.pago            = request.POST.get('pago',None)
        if request.POST.get('pacote',None) == 'True':
            new_agendamento.valor = float(request.POST.get('valor', None))/int(sessoes)
        else:
            new_agendamento.valor       = request.POST.get('valor', None)
        new_agendamento.pacote          = request.POST.get('pacote',None)
        new_agendamento.sala_id         = request.POST.get('sala',None)
        new_agendamento.status          = request.POST.get('status', None)
        new_agendamento.convenio_id     = request.POST.get('convenio', None)
        if Agendamento.objects.filter(data=new_dates,paciente_id = request.POST.get('paciente',None),
            profissional_id = request.POST.get('profissional',None),
            hora_inicio = request.POST.get('hora_inicio',None)).exists():
            pass           
        else: 
            new_agendamento.save()
   
    data = {}
    return JsonResponse(data)


#listagem do full calendar 
def agenda(request):
    #if profissinal estiver logado eu listo apenas seus pacientes
    if Profissional.prof_objects.filter(user=request.user,tipo=2).exists():
         paciente      = Paciente.objects.filter(
            profissional=Profissional.prof_objects.get(
                user=request.user,tipo=2).id).values('id', 'nome','telefone','convenio__nome')
    else:
        paciente      = Paciente.objects.all().values('id', 'nome','telefone','convenio__nome')
    profissional      = Profissional.objects.filter(tipo=2).values('id',
     'nome','sobrenome').exclude(user__username='admin')
    sala              = Sala.objects.all().values('id', 'nome')
    convenio          = Convenio.objects.all().values('id', 'nome')
    
    agenda            = ""
    infoProfissional  = ""
    id_profissional   = ""
    verifica_prof_log = Profissional.prof_objects.filter(
        user=request.user,tipo=2)

    if request.GET.get('profissional'):
        profissional_search = request.GET.get('profissional')
        infoProfissional    = Profissional.objects.get(
        id=profissional_search) #exibe informações
        agenda              = Agendamento.objects.select_related('paciente',
            'convenio','sala','profissional').filter(
            profissional_id=profissional_search).exclude(status='CC')
    elif verifica_prof_log.exists():
        agenda              = Agendamento.objects.select_related('paciente',
            'convenio','sala','profissional').filter(
            profissional_id = Profissional.prof_objects.get(
                user=request.user,tipo=2).id).exclude(status='CC')
        id_profissional     = Profissional.prof_objects.get(
                user=request.user,tipo=2).id
    #armazena os dados de atuação do profisional logado
    lista = []
    if verifica_prof_log.exists():
        pff = Profissional.objects.get(user=request.user,tipo=2)      
        for i in pff.area_atuacao.all():
            lista.append(i.get_id_display())
    else:
        pass
            #print (i)

    context = {
        'agenda':agenda,
        'pacientes':paciente,
        'profissionais':profissional,
        'salas':sala,
        'convenios':convenio,
        'lista_fichas_options':lista,
        'infoProfissional':infoProfissional,
        'verifica_prof_log':verifica_prof_log,
        'id_profissional':id_profissional,

    }
    return render(request,'agenda/agenda.html',context)


def remove_agend_calendar(request):
    id = request.GET.get("id",None)
    evnte = Agendamento.objects.get(id=id)
    evnte.delete()
    data = {}
    return JsonResponse(data)


def update_agend_calendar(request,pk):
    print('o id',pk)
    data_form  = datetime.strptime(
        request.POST.get("data", None),'%d/%m/%Y').strftime('%Y-%m-%d')
    agendamento                 = Agendamento.objects.get(id=pk)
    agendamento.data            = data_form
    agendamento.hora_inicio     = request.POST.get('hora_inicio',None)
    agendamento.hora_fim        = request.POST.get('hora_fim',None)
    agendamento.status          = request.POST.get('status',None)
    agendamento.telefone        = request.POST.get('telefone',None)
    agendamento.valor           = request.POST.get('valor',None)
    agendamento.observacao      = request.POST.get('observacao',None)
    agendamento.pago            = request.POST.get('pago',None)
    agendamento.pacote          = request.POST.get('pacote',None)
    agendamento.sala_id         = request.POST.get('sala',None)
    agendamento.paciente_id     = request.POST.get('paciente',None)
    agendamento.profissional_id = request.POST.get('profissional',None)
    agendamento.convenio_id     = request.POST.get('convenio', None)
    agendamento.save()    
    data = {}
    return JsonResponse(data)


def adicionar_paciente_calendar(request):
    data_nascimento          = datetime.strptime(
        request.POST.get("nascimento", None),'%d/%m/%Y').strftime('%Y-%m-%d')
    nome                     = request.POST.get('nome',None)
    cpf                      = request.POST.get('cpf',None)
    paciente                 = Paciente()
    paciente.nome            = nome
    paciente.telefone        = request.POST.get('telefone',None)
    paciente.data_nascimento = data_nascimento
    paciente.convenio_id     = request.POST.get('convenio',None)
    paciente.cpf             = cpf
    if request.POST.get('possui_cpf',None) == 'on':
        paciente.possui_cpf  = True
    else:
        paciente.possui_cpf  = False
    
    if Paciente.objects.filter(cpf__iexact=cpf).exists() and cpf != None:
        messages.error(request,'Erro: Paciente Já Existente na Base de Dados! ')
    else:
        paciente.save()
        paciente.profissional.add(*request.POST.getlist('profissional',None))
        paciente.save()
        messages.success(request,'Paciente Cadastrado com Sucesso! ')
    data = {}
    return redirect('agenda')
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           Crud de Agenda Padrão
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

@login_required
def agendamento(request):
    #armazena os dados de atuação do profisional logado
    lista = []
    #atendente e profissional
    #pf é querysets para exibir profissionais no template para o filtro
    pf                  = Profissional.prof_objects.filter(tipo=2).values('id',
     'nome','sobrenome').exclude(user__username='admin')
    #at querysets para fazer condição no template e determinar o que deve ser exibido
    at                  = Profissional.prof_objects.filter(user=request.user,tipo=1)
    profissional        = Profissional.prof_objects.filter(user=request.user,tipo=2)

    if profissional.exists():
        pff = Profissional.objects.get(user=request.user,tipo=2)      
        for i in pff.area_atuacao.all():
            lista.append(i.get_id_display())
    else:
        pass
            #print (i)
    date_range          = None
    start_date_string   = None
    end_date_string     = None
    agendamentos        = None
    agenda_profissional = None
    #verifica quem esta logado, se for profissional retorna True e mostra apenas os agendamentos dele liberados
    if profissional.exists():
        if request.GET.get('date_ranger'):
            date_range        = request.GET.get('date_ranger')
            start_date_string = datetime.strptime(date_range.split(' / ')[0],'%d/%m/%Y').strftime('%Y-%m-%d')
            end_date_string   = datetime.strptime(date_range.split(' / ')[1],'%d/%m/%Y').strftime('%Y-%m-%d')
            status            = request.GET.get('status')
            paciente          = request.GET.get('paciente')
            if status != None:
                agenda_profissional = Agendamento.objects.select_related('paciente',
            'convenio','sala','profissional').filter(data__range=(start_date_string,end_date_string),
                status=status,paciente__nome__icontains=paciente,profissional__user=request.user)
            else:
                agenda_profissional = Agendamento.objects.select_related('paciente',
            'convenio','sala','profissional').filter(data__range=(start_date_string,end_date_string),
                paciente__nome__icontains=paciente,profissional__user=request.user)
        else:
            today = timezone.now()
            agenda_profissional = Agendamento.objects.select_related('paciente',
            'convenio','sala','profissional').filter(profissional__user=request.user,
                    data__day=today.day,data__month=today.month)
    else:
        #se for False retorna todos os agendamentos independente de admin ou atendente
        if request.GET.get('date_ranger'):
            date_range          = request.GET.get('date_ranger')
            start_date_string   = datetime.strptime(date_range.split(' / ')[0],'%d/%m/%Y').strftime('%Y-%m-%d')
            end_date_string     = datetime.strptime(date_range.split(' / ')[1],'%d/%m/%Y').strftime('%Y-%m-%d')
            profissional_search = request.GET.get('profissional')
            status              = request.GET.get('status')
            paciente            = request.GET.get('paciente')
            if status != None:
                agendamentos = Agendamento.objects.select_related('paciente',
            'convenio','sala','profissional').filter(data__range=(start_date_string,end_date_string),
                profissional__nome__icontains=profissional_search,status=status,paciente__nome__icontains=paciente)
            else:
                agendamentos = Agendamento.objects.select_related('paciente',
            'convenio','sala','profissional').filter(data__range=(start_date_string,end_date_string),
                profissional__nome__icontains=profissional_search,paciente__nome__icontains=paciente)
        else:
            today = timezone.now()
            agendamentos = Agendamento.objects.select_related('paciente',
            'convenio','sala','profissional').filter(data__day=today.day,
                data__month=today.month)
     
    context = {
        'pf':pf,
        'at':at,
        'profissional':profissional,
        'agendamentos':agendamentos,
        'af':agenda_profissional,
        'lista_fichas_options':lista,

    }
    return render(request,'agenda/agendamentos.html',context)

@login_required
def add_agendamento(request):
    form = AgendaForm(request.POST or None)
    #if profissinal estiver loado eu listo apenas seus pacientes
    if Profissional.prof_objects.filter(user=request.user,tipo=2).exists():
        form.fields['paciente'].queryset = Paciente.objects.filter(
            profissional=Profissional.prof_objects.get(
                user=request.user,tipo=2).id)

    if form.is_valid():
        date_form = request.POST.get('data')
        data_now  = datetime.strptime(date_form,'%d/%m/%Y').strftime('%Y-%m-%d')
        new_dates = datetime.strptime(data_now, '%Y-%m-%d').date()
        condicao = True
        sessoes  = int(request.POST.get('sessoes'))
        for i in range(0,sessoes):
            if i != 0:
                new_dates += relativedelta(days=7)
           
            new_agendamento              = Agendamento()
            new_agendamento.data         = new_dates
            new_agendamento.hora_inicio  = form.cleaned_data.get('hora_inicio')
            new_agendamento.hora_fim     = form.cleaned_data.get('hora_fim')
            new_agendamento.sala         = form.cleaned_data.get('sala')
            new_agendamento.paciente     = form.cleaned_data.get('paciente')
            new_agendamento.convenio     = form.cleaned_data.get('convenio')
            new_agendamento.profissional = form.cleaned_data.get('profissional')
            new_agendamento.telefone     = form.cleaned_data.get('telefone')
            if form.cleaned_data.get('pacote') == True:
                new_agendamento.valor        = float(form.cleaned_data.get('valor'))/int(sessoes)
            else:
                new_agendamento.valor    = form.cleaned_data.get('valor')
            new_agendamento.pago         = form.cleaned_data.get('pago')
            new_agendamento.pacote       = form.cleaned_data.get('pacote')
            new_agendamento.save()
        messages.success(request,'Agendamento Cadastrado com Sucesso! ')
        return redirect('agendamentos')
            
    return render(request,'agenda/adicionar_agendamento.html',{'form':form,})

@login_required
def atender_recepcao(request,pk):
    agenda               = Agendamento.objects.get(pk=pk)
    form                 = AgendaForm(request.POST or None,instance = agenda)
    lista_guias_paciente = Guia.objects.filter(paciente_id=agenda.paciente.id,quantidade__gte=1,ativo=True)
    lista_guias          = []
    for g in lista_guias_paciente:
        lista_guias.append(g)
    if form.is_valid():
        form.save(commit=False)
        if agenda.convenio.id != 1:
            #testa se é diferente de particular
            if request.POST['status'] == 'FH' or request.POST['status'] == 'FN' or request.POST['status'] == 'AR':
                if lista_guias_paciente.exists():  
                    #if request.POST['lista_guias_field'] != None:
                    number = (request.POST['lista_guias_field'].split('|')[:][0])
                    print("number",number)
                    guia = Guia.objects.get(
                        paciente_id=agenda.paciente.id,
                        quantidade__gte=1,
                        ativo=True,
                        numero=number.replace(" ","")
                    )
                    print(guia,'Query de guias correspondentes') 
                    #verifica vencimento
                    if not datetime.strptime(str(guia.validade),'%Y-%m-%d') < datetime.strptime(
                        datetime.now().strftime("%Y-%m-%d"),'%Y-%m-%d'):
                        
                        guia.quantidade -= 1
                        guia.save()
                        form.save()
                        #converte datas
                        data_now  = datetime.strptime(request.POST.get('data'),'%d/%m/%Y').strftime('%Y-%m-%d')
                        new_date  = datetime.strptime(data_now, '%Y-%m-%d').date()
                        
                        #cria um atendimento baseado nos dados do agendamento feito
                        Atendimento.objects.create(
                            tipo=request.POST['status'],
                            data=new_date,
                            paciente_id=request.POST['paciente'],
                            hora_inicio=request.POST['hora_inicio'],
                            hora_fim=request.POST['hora_fim'],
                            profissional_id=request.POST['profissional'],
                            convenio_id=request.POST['convenio'],
                            procedimento_id=guia.procedimento.id,
                            guia_id=guia.id,
                        )
                        #print('criou agenda')
                        #finaliza a guia se tiver menor que zero a quantidade
                        if guia.quantidade < 1:
                            guia.ativo = False
                            guia.save()
                        
                        messages.success(request,'Agendamento Atualizado com Sucesso! ')
                        return redirect('agendamentos')
                    else:
                        messages.warning(request,'Esse Guia está vencida! ')
                else:
                    #print('dentro do else em condição em guia')
                    messages.error(request,'Atenção...esse paciente não possui Uma Guia para Decrementar')
            else:
                form.save()
                messages.success(request,'Agendamento Atualizado com Sucesso! ')
                return redirect('agendamentos')  
        else:
            form.save()
            #converte datas
            data_now  = datetime.strptime(request.POST.get('data'),'%d/%m/%Y').strftime('%Y-%m-%d')
            new_date  = datetime.strptime(data_now, '%Y-%m-%d').date()
            #cria um atendimento baseado nos dados do agendamento feito
            Atendimento.objects.create(
                tipo='AR',
                data=new_date,
                paciente_id=request.POST['paciente'],
                hora_inicio=request.POST['hora_inicio'],
                hora_fim=request.POST['hora_fim'],
                profissional_id=request.POST['profissional'],
                convenio_id=request.POST['convenio'],
            )
            messages.success(request,'Agendamento Atualizado com Sucesso! ')
            return redirect('agendamentos')
    return render(request,'agenda/atender_recepcao.html',{'form':form,'guias_views':lista_guias,'agendamento':agenda})


@login_required
def update_agendamento(request,pk):
    agenda               = Agendamento.objects.get(pk=pk)
    form                 = AgendaForm(request.POST or None,instance = agenda)
    lista_guias_paciente = Guia.objects.filter(paciente_id=agenda.paciente.id,quantidade__gte=1,ativo=True)
    lista_guias          = []
    for g in lista_guias_paciente:
        lista_guias.append(g)
    if form.is_valid():
        form.save(commit=False)
        if agenda.convenio.id != 1:
            #testa se é diferente de particular
            if request.POST['status'] == 'FH' or request.POST['status'] == 'FN' or request.POST['status'] == 'AR':
                if lista_guias_paciente.exists():                
                    #if request.POST['lista_guias_field'] != None:
                    number = (request.POST['lista_guias_field'].split('|')[:][0])
                    print("number",number)
                    guia = Guia.objects.get(
                        paciente_id=agenda.paciente.id,
                        quantidade__gte=1,
                        ativo=True,
                        numero=number.replace(" ","")
                    )
                    #verifica vencimento
                    if not datetime.strptime(str(guia.validade),'%Y-%m-%d') < datetime.strptime(
                        datetime.now().strftime("%Y-%m-%d"),'%Y-%m-%d'):
                        guia.quantidade -= 1
                        guia.save()
                        form.save()
                        #converte datas
                        data_now  = datetime.strptime(request.POST.get('data'),'%d/%m/%Y').strftime('%Y-%m-%d')
                        new_date  = datetime.strptime(data_now, '%Y-%m-%d').date()
                        
                        #cria um atendimento baseado nos dados do agendamento feito
                        Atendimento.objects.create(
                            tipo=request.POST['status'],
                            data=new_date,
                            paciente_id=request.POST['paciente'],
                            hora_inicio=request.POST['hora_inicio'],
                            hora_fim=request.POST['hora_fim'],
                            profissional_id=request.POST['profissional'],
                            convenio_id=request.POST['convenio'],
                            procedimento_id=guia.procedimento.id,
                            guia_id=guia.id,
                        )
                        #print('criou agenda')
                        #finaliza a guia se tiver menor que zero a quantidade
                        if guia.quantidade < 1:
                            guia.ativo = False
                            guia.save()
                        
                        messages.success(request,'Agendamento Atualizado com Sucesso! ')
                        return redirect('agendamentos')
                    else:
                        messages.warning(request,'Esse Guia está vencida! ')
                else:
                    #print('dentro do else em condição em guia')
                    messages.error(request,'Atenção...esse paciente não possui Uma Guia para Decrementar')
            else:
                form.save()
                messages.success(request,'Agendamento Atualizado com Sucesso! ')
                return redirect('agendamentos')  
        else:
            form.save()
            #converte datas
            data_now  = datetime.strptime(request.POST.get('data'),'%d/%m/%Y').strftime('%Y-%m-%d')
            new_date  = datetime.strptime(data_now, '%Y-%m-%d').date()
            #cria um atendimento baseado nos dados do agendamento feito
            Atendimento.objects.create(
                tipo='AR',
                data=new_date,
                paciente_id=request.POST['paciente'],
                hora_inicio=request.POST['hora_inicio'],
                hora_fim=request.POST['hora_fim'],
                profissional_id=request.POST['profissional'],
                convenio_id=request.POST['convenio'],
            )
            messages.success(request,'Agendamento Atualizado com Sucesso! ')
            return redirect('agendamentos')
    return render(request,'agenda/adicionar_agendamento.html',{'form':form,'guias_views':lista_guias})
"""
@login_required
def update_agendamento(request,pk):
    agenda = Agendamento.objects.get(pk=pk)
    form = AgendaForm(request.POST or None,instance = agenda)
    if form.is_valid():
        date_form  = request.POST.get('data')
        data_now  = datetime.strptime(date_form,'%d/%m/%Y').strftime('%Y-%m-%d')
        agendamento = Agendamento.objects.filter(data=data_now,status__in=['AG', 'DM']).order_by(
            'hora_inicio','hora_fim'
        )
        condicao = True
        for i in agendamento:
            hour = ":00"
            hora_inicio = request.POST['hora_inicio']+hour
            hora_fim = request.POST['hora_fim']+hour

            if((int(i.sala.id) == int(request.POST['sala'])) and (str(i.data) == str(data_now))  
                and (str(hora_inicio) >= (str(i.hora_inicio)) and str(hora_inicio) < str(i.hora_fim))): 
                messages.warning(request,'Esse Agendamento não pode ser salvo pq ja existe um igual no banco:( ')
                condicao = False
                break
            elif((int(i.paciente.id) == int(request.POST['paciente'])) and (str(i.data) == str(data_now))  
                and (str(hora_inicio) >= (str(i.hora_inicio)) and str(hora_inicio) < str(i.hora_fim))): 
                messages.warning(request,'Esse Agendamento não pode ser salvo pq ja existe um igual no banco:( ')
                condicao = False
                break
            elif((int(i.profissional.id) == int(request.POST['profissional'])) and (str(i.data) == str(data_now))  
                and (str(hora_inicio) >= (str(i.hora_inicio)) and str(hora_inicio) < str(i.hora_fim))): 
                messages.warning(request,'Esse Agendamento não pode ser salvo pq ja existe um igual no banco:( ')
                condicao = False
                break
            else:
                condicao = True
                continue
        if condicao == True:
            form.save()
            if 'SaveAddOther' in request.POST:
                hora_inicio  = form.cleaned_data.get('hora_inicio')
                hora_fim     = form.cleaned_data.get('hora_fim')
                sala         = form.cleaned_data.get('sala')
                paciente     = form.cleaned_data.get('paciente')
                convenio     = form.cleaned_data.get('convenio')
                profissional = form.cleaned_data.get('profissional')
                telefone     = form.cleaned_data.get('telefone')

                form = AgendaForm(initial={
                    'hora_inicio': hora_inicio,
                    'hora_fim': hora_fim,
                    'sala': sala,
                    'paciente': paciente,
                    'convenio': convenio,
                    'profissional': profissional,
                    'telefone': telefone,
                })
                messages.success(request,'Agendamento Atualizado com Sucesso! ')
            elif 'Save' in request.POST:
                messages.success(request,'Agendamento Atualizado com Sucesso! ')
            return redirect('agendamentos')            
    return render(request,'agenda/adicionar_agendamento.html',{'form':form})
"""

@login_required
def agendamento_detalhe(request,pk):
    agendamento = get_object_or_404(Agendamento,pk=pk)
    return render(request,'agenda/agendamento_detalhe.html',{'agenda':agendamento})

@login_required
def cancel_agendamento(request,pk):
    agenda = get_object_or_404(Agendamento,pk=pk)
    agenda.sala = None
    agenda.status = 'CC'
    agenda.save()
    messages.info(request,'Agendamento Cancelado! ')
    return redirect('agendamentos')

#função que serve de pre-atendimento
@login_required
def liberar_agendamento(request,pk):
    agenda = get_object_or_404(Agendamento,pk=pk)
    """
    if agenda.status == 'AG':
        agenda.liberado = True
        agenda.status   = 'AD'
        agenda.save()
    """
        #messages.success(request,'Pré Atendimento....PDF de Confirmação de Chegada Liberado Para Impressão! ')
        #redireciona para imprimir o comprovante em PDF
    return redirect('liberar_paciente_pdf',pk)
    #return redirect('agendamentos')

@login_required
def desmarcar_agendamento(request,pk):
    agenda = get_object_or_404(Agendamento,pk=pk)
    if agenda.status =='AG':
        agenda.status = 'DM'
        agenda.save()
        messages.info(request,'O Agendamento foi Desmarcado! ')
    else:
        agenda.status = 'AG'
        agenda.save()
        messages.info(request,'O Agendamento foi Remarcado! ')
    return redirect('agendamentos')

def deletar_agendamento(request,pk):
    agenda = get_object_or_404(Agendamento,pk=pk)
    agenda.delete()
    messages.success(request,'Agendamento Deletado com Sucesso! ')
    return redirect('agendamentos')
