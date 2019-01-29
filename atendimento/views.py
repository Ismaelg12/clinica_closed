# -*- coding: utf-8 -*-
from django.utils import timezone
#import datetime
from datetime import timedelta, datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from atendimento.forms import AgendaForm,AtendimentoForm
from atendimento.models import Agendamento,Atendimento,Guia
from core.models import Sala,Convenio,Procedimento
from pacientes.models import Paciente
from controle_usuarios.models import Profissional
from django.contrib.auth.decorators import login_required
from django.contrib import messages

'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           Crud de Agenda
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
@login_required
def agendamento(request):
    #atendente e profissional
    #pf é querysets para exibir profissionais no template para o filtro
    pf                  = Profissional.objects.filter(tipo=2)
    #at querysets para fazer condição no template e determinar o que deve ser exibido
    at                  = Profissional.objects.filter(user=request.user,tipo=1)
    profissional        = Profissional.objects.filter(user=request.user,tipo=2)
    date_range          = None
    start_date_string   = None
    end_date_string     = None
    agendamentos        = None
    agenda_profissional = None
    #verifica quem esta logado, se for profissional retorn True e mostra apenas os agendamentos dele liberados
    if profissional.exists():
        if request.GET.get('date_ranger'):
            date_range        = request.GET.get('date_ranger')
            start_date_string = datetime.strptime(date_range.split(' / ')[0],'%d/%m/%Y').strftime('%Y-%m-%d')
            end_date_string   = datetime.strptime(date_range.split(' / ')[1],'%d/%m/%Y').strftime('%Y-%m-%d')
            status            = request.GET.get('status')
            paciente          = request.GET.get('paciente')
            if status != None:
                agenda_profissional = Agendamento.objects.filter(data__range=(start_date_string,end_date_string),
                status=status,paciente__nome__icontains=paciente,profissional__user=request.user,liberado=True)
            else:
                agenda_profissional = Agendamento.objects.filter(data__range=(start_date_string,end_date_string),
                paciente__nome__icontains=paciente,profissional__user=request.user,liberado=True)
        else:
            today = timezone.now()
            agenda_profissional = Agendamento.objects.filter(profissional__user=request.user,liberado=True,
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
                agendamentos = Agendamento.objects.filter(data__range=(start_date_string,end_date_string),
                profissional__nome__icontains=profissional_search,status=status,paciente__nome__icontains=paciente)
            else:
                agendamentos = Agendamento.objects.filter(data__range=(start_date_string,end_date_string),
                profissional__nome__icontains=profissional_search,paciente__nome__icontains=paciente)
        else:
            today = timezone.now()
            agendamentos = Agendamento.objects.filter(data__day=today.day,
                data__month=today.month)
    context = {
        'pf':pf,
        'at':at,
        'profissional':profissional,
        'agendamentos':agendamentos,
        'af':agenda_profissional,

    }
    return render(request,'agenda/agendamentos.html',context)
"""
@login_required
def add_agendamento(request):
    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Agendamento Cadastrado com Sucesso! ')
            return redirect('agendamentos')
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = AgendaForm()

    context = {
        'form': form, 
    }
    data['html_form'] = render_to_string('agenda/includes/add_agendamento.html',
        context,
        request=request
    )
    return JsonResponse(data)
"""

@login_required
def add_agendamento(request):
    form = AgendaForm(request.POST)
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
                messages.success(request,'Esse Agendamento não pode ser salvo pq ja existe um igual no banco:( ')
                condicao = False
                break
            elif((int(i.paciente.id) == int(request.POST['paciente'])) and (str(i.data) == str(data_now))  
                and (str(hora_inicio) >= (str(i.hora_inicio)) and str(hora_inicio) < str(i.hora_fim))): 
                messages.success(request,'Esse Agendamento não pode ser salvo pq ja existe um igual no banco:( ')
                condicao = False
                break
            elif((int(i.profissional.id) == int(request.POST['profissional'])) and (str(i.data) == str(data_now))  
                and (str(hora_inicio) >= (str(i.hora_inicio)) and str(hora_inicio) < str(i.hora_fim))): 
                messages.success(request,'Esse Agendamento não pode ser salvo pq ja existe um igual no banco:( ')
                condicao = False
                break
            else:
                condicao = True
                continue
        if condicao == True:
            form.save()
            if 'SaveAddOther' in request.POST:
                hora_inicio = form.cleaned_data.get('hora_inicio')
                hora_fim = form.cleaned_data.get('hora_fim')
                sala = form.cleaned_data.get('sala')
                paciente = form.cleaned_data.get('paciente')
                convenio = form.cleaned_data.get('convenio')
                profissional = form.cleaned_data.get('profissional')
                telefone = form.cleaned_data.get('telefone')

                form = AgendaForm(initial={
                    'hora_inicio': hora_inicio,
                    'hora_fim': hora_fim,
                    'sala': sala,
                    'paciente': paciente,
                    'convenio': convenio,
                    'profissional': profissional,
                    'telefone': telefone,
                })
                messages.success(request,'Agendamento Cadastrado com Sucesso! ')
            elif 'Save' in request.POST:
                messages.success(request,'Agendamento Cadastrado com Sucesso! ')
                return redirect('agendamentos')
    return render(request,'agenda/adicionar_agendamento.html',{'form':form})

@login_required
def update_agendamento(request,pk):
    agenda = Agendamento.objects.get(pk=pk)
    form = AgendaForm(request.POST or None,instance = agenda)
    if form.is_valid():
        form.save()
        messages.success(request,'Agendamento Atualizado com Sucesso! ')
        return redirect('agendamentos')
    return render(request,'agenda/adicionar_agendamento.html',{'form':form})
"""
@login_required
def update_agendamento(request,pk):
    agenda = Agendamento.objects.get(pk=pk)
    data = dict()
    form = AgendaForm(request.POST or None,instance = agenda)
    if form.is_valid():
        form.save()
        messages.success(request,'Agendamento Atualizado com Sucesso! ')
        return redirect('agendamentos')
        data['form_is_valid'] = True
    else:
        data['form_is_valid'] = False
    context = {
        'form': form,
    }
    data['html_form'] = render_to_string('agenda/includes/update_agendamento.html',
        context,
        request=request
    )
    return JsonResponse(data)
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
    messages.success(request,'Agendamento Cancelado! ')
    return redirect('agendamentos')

@login_required
def liberar_agendamento(request,pk):
    agenda = get_object_or_404(Agendamento,pk=pk)
    agenda.liberado = True
    agenda.save()
    messages.success(request,'Agendamento Liberado para Atendimento pelo Profissional! ')
    return redirect('agendamentos')

@login_required
def desmarcar_agendamento(request,pk):
    agenda = get_object_or_404(Agendamento,pk=pk)
    agenda.status = 'DM'
    agenda.save()
    messages.success(request,'Agendamento Desmarcado! ')
    return redirect('agendamentos')
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           Crud de Atendimentos
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
@login_required
def atendimentos(request):
    pf = Profissional.objects.filter(tipo=2)
    at = Profissional.objects.filter(user=request.user,tipo=1)
    if request.method == "POST":
        date_range        = request.POST.get('date_ranger')
        start_date_string = datetime.strptime(date_range.split(' / ')[0],'%d/%m/%Y').strftime('%Y-%m-%d')
        end_date_string   = datetime.strptime(date_range.split(' / ')[1],'%d/%m/%Y').strftime('%Y-%m-%d')
        
        profissional      = request.POST.get('profissional')
        tipo_atendimento  = request.POST.get('tipo')
        if tipo_atendimento != None:
            atendimento = Atendimento.objects.filter(data__range=(start_date_string,end_date_string),
                profissional__nome__icontains=profissional,tipo=tipo_atendimento)
        else:
            atendimento = Atendimento.objects.filter(data__range=(start_date_string,end_date_string),
                profissional__nome__icontains=profissional)
    else:
        #exibe todos os atendiementos quando abrir a pagina
        atendimento = Atendimento.objects.all()
    context = {
        'pf':pf,
        'at':at,
        'atendimentos':atendimento,
    }
    return render(request,'atendimento/atendimentos.html',context)

@login_required
def atendimento_add(request,pk):
    pf = Profissional.objects.get(user=request.user)
    agendamento = get_object_or_404(Agendamento,pk=pk)
    form = AtendimentoForm(request.POST or None,initial={
        'paciente':agendamento.paciente,
        #'convenio':agendamento.convenio,
        'profissional':pf.id,
    })
    if form.is_valid():
        at = form.save(commit=False)
        at.guia.quantidade -=1
        at.guia.save()
        agendamento.status = "AT"
        agendamento.save()
        at.save()
        messages.success(request,'Atendimento Adicionado com Sucesso! ')
        return redirect('atendimentos')
    return render(request,'atendimento/adicionar_atendimento.html',{'form':form})

@login_required
def atendimento_update(request,pk):
    atendimento = get_object_or_404(Atendimento,pk=pk)
    form = AtendimentoForm(request.POST or None,instance = atendimento)
    if form.is_valid():
        form.save()
        messages.success(request,'Atendimento Atualizado com Sucesso! ')
        return redirect('atendimentos')
    return render(request,'atendimento/adicionar_atendimento.html',{'form':form})

@login_required
def excluir_atendimento(request,pk):
    atendimento = get_object_or_404(Atendimento,pk=pk)
    atendimento.delete()
    messages.success(request,'Excluido com Sucesso! ')
    return redirect('atendimentos')
    
@login_required
def atendimento_detalhe(request,pk):
    atendimento = get_object_or_404(Atendimento,pk=pk)
    return render(request,'atendimento/atendimento_detalhe.html',{'atendimento':atendimento})

@login_required
def load_procedimentos_guias(request):
    convenio_id   = request.GET.get('convenio')
    paciente_id   = request.GET.get('paciente')
    guias         = Guia.objects.filter(paciente=paciente_id)
    procedimentos = Procedimento.objects.filter(convenio=convenio_id).order_by('nome')
    context = {
        'procedimentos': procedimentos,
        'guias': guias
    }
    return render(request, 'atendimento/procedimentos.html',context)
"""
def load_guias(request):
    country_id = request.GET.get('paciente')
    cities = Guia.objects.filter(paciente=country_id)
    return render(request, 'atendimento/guias.html', {})
"""