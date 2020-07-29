# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from pacientes.models import Paciente
from controle_usuarios.models import Profissional
from atendimento.models import Atendimento,Guia,Avaliacao
from agenda.models import Agendamento
from financeiro.models import ContaReceber
from django.contrib import messages
from pacientes.forms import PacienteForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse
from atendimento.models import *
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                          Crud de Pacientes/Clientes
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

class PacienteCreateView(LoginRequiredMixin,CreateView):
    model         = Paciente
    template_name = 'adicionar_paciente.html'
    form_class    = PacienteForm
    success_url   = reverse_lazy('lista_pacientes')
    #salvar e adicionar novo 
    def post(self, request, *args, **kwargs):
        save_action = None
        if "cancelar" in request.POST:
            return HttpResponseRedirect(reverse('lista_pacientes'))
        else:
            save_action = super(PacienteCreateView, self).post(request, *args, **kwargs)
        if "adicionar_outro" in request.POST:
            messages.success(request,'Paciente Cadastrado com Sucesso! ')
            return HttpResponseRedirect(reverse('add_paciente'))
        return save_action


class PacienteListView(LoginRequiredMixin,ListView):
    model               = Paciente
    template_name       = 'pacientes.html'
    context_object_name = 'pacientes'
    paginate_by = 50

    def get_queryset(self, **kwargs):
        queryset = Paciente.objects.select_related(
            'convenio').prefetch_related('profissional').all()
        if self.request.GET.get('paciente'):
            paciente_search = self.request.GET.get('paciente')
            queryset = Paciente.objects.filter(
                nome__icontains=paciente_search).select_related(
            'convenio').prefetch_related('profissional').order_by('id')
        return queryset


    def get_context_data(self, *args, **kwargs):
        context = super(PacienteListView, self).get_context_data(*args, **kwargs)
        context['profissional_logado'] = Profissional.objects.filter(
            user=self.request.user,tipo=2
        )
        context['paciente_clinico'] = Paciente.objects.select_related(
            'convenio').prefetch_related('profissional').filter(
            profissional__user=self.request.user)
        #if tiver busca ele filtra os meus pacientes
        if self.request.GET.get('paciente'):
            paciente_search = self.request.GET.get('paciente')
            context['paciente_clinico'] = Paciente.objects.select_related(
            'convenio').prefetch_related('profissional').filter(
                nome__icontains=paciente_search,profissional__user=self.request.user).order_by('id')
        return context

        
class PacienteUpdateView(LoginRequiredMixin,UpdateView):
    model = Paciente
    template_name = 'adicionar_paciente.html'
    form_class    = PacienteForm
    success_url   = reverse_lazy('lista_pacientes')


@login_required 
def PacienteDeleteView(request,pk):
    try :
        paciente = get_object_or_404(Paciente, pk=pk).delete()
        messages.error(request,'Paciente Deletado Com Sucesso.')
    except ProtectedError:
        messages.warning(request,
         "você não pode deletar esse paciente porque ele tem atendimentos ou agendamentos feitos")
    return redirect('lista_pacientes')


class PacienteDetailView(LoginRequiredMixin,DetailView):
    model = Paciente
    template_name = 'paciente_detalhe.html'
    context_object_name = 'paciente'


@login_required 
def paciente_historico(request,pk):
    profissional = ""
    atendente    = Profissional.prof_objects.filter(user=request.user,tipo=1)
    paciente              = get_object_or_404(Paciente,pk=pk)
    ######################################################

    #quesyset apenas para condição no template
    if atendente.exists() or request.user.is_superuser:
        #não faz nada :)
        pass
    else:
        profissional = Profissional.prof_objects.get(user=request.user,tipo=2)

    #lista todos os atendimentos na 1ª aba e 2ª aba linha do tempo
    if profissional:
        atendimentos    = Atendimento.objects.filter(paciente=paciente,profissional_id=profissional.id)
        #evolucões       
        ficha_evolucao  =  Evolucao.objects.filter(atendimento__paciente=paciente.id,atendimento__profissional_id=profissional.id)

        #avaliações
        ficha_avaliacao = Avaliacao.objects.filter(atendimento__paciente=paciente.id,atendimento__profissional_id=profissional.id)
    else:
        atendimentos      = Atendimento.objects.filter(paciente=paciente)
        ficha_evolucao    =  Evolucao.objects.filter(atendimento__paciente=paciente.id)
        ficha_avaliacao   = Avaliacao.objects.filter(atendimento__paciente=paciente.id)

    atendimentos_count    = Atendimento.objects.filter(paciente=paciente).count()
    agendamentos_count    = Agendamento.objects.filter(paciente=paciente).count()
    agendamentos_FJ_count = Agendamento.objects.filter(paciente=paciente,status='FJ').count()
    agendamentos_FH_count = Agendamento.objects.filter(paciente=paciente,status='FH').count()
    agendamentos_FN_count = Agendamento.objects.filter(paciente=paciente,status='FN').count()
    agendamentos_CC_count = Agendamento.objects.filter(paciente=paciente,status='CC').count()
    atendimento_evolucao  = Atendimento.objects.filter(paciente=paciente,).count()
    atendimento_avaliacao = Atendimento.objects.filter(paciente=paciente,).count()
    guias                 = Guia.objects.filter(paciente=paciente).order_by('-validade')
    contas                = ContaReceber.objects.filter(paciente=paciente).order_by('-data')

    context = {
        'profissional':profissional,
        'atendimentos_count':atendimentos_count,
        'evolucao':atendimento_evolucao,
        'avaliacao':atendimento_avaliacao,
        'paciente':paciente,
        'agendamentos':agendamentos_count,
        'agendamentos_FJ_count':agendamentos_FJ_count,
        'agendamentos_FH_count':agendamentos_FH_count,
        'agendamentos_FN_count':agendamentos_FN_count,
        'agendamentos_CC_count':agendamentos_CC_count,
        'linha_do_tempo':atendimentos,
        'guias':guias,
        'contas':contas,
        ##########FICHAS PARA O HISTORICO RENDERIZADAS MANUALMENTE#######
        'ficha_evolucao':ficha_evolucao,
        'ficha_avaliacao':ficha_avaliacao,
    }
    return render(request,'historico.html',context)