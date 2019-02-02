# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from pacientes.models import Paciente
from controle_usuarios.models import Profissional
from atendimento.models import Atendimento,Agendamento,Guia
from financeiro.models import ContaReceber
from django.contrib import messages
from pacientes.forms import PacienteForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import ProtectedError
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

class PacienteListView(LoginRequiredMixin,ListView):
    model               = Paciente
    template_name       = 'pacientes.html'
    context_object_name = 'pacientes'

class PacienteUpdateView(LoginRequiredMixin,UpdateView):
    model = Paciente
    template_name = 'adicionar_paciente.html'
    form_class    = PacienteForm
    success_url   = reverse_lazy('lista_pacientes')

@login_required 
def PacienteDeleteView(request,pk):
    try :
        paciente = get_object_or_404(Paciente, pk=pk).delete()
        messages.error(request, 'Paciente Deletado Com Sucesso.')
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
    #quesyset apenas para condição no template
    profissional          = Profissional.objects.filter(user=request.user,tipo=2)
    paciente              = get_object_or_404(Paciente,pk=pk)
    agendamentos_count    = Agendamento.objects.filter(paciente=paciente).count()
    agendamentos_DM_count = Agendamento.objects.filter(paciente=paciente,status='DM').count()
    agendamentos_CC_count = Agendamento.objects.filter(paciente=paciente,status='CC').count()
    atendimentos          = Atendimento.objects.filter(paciente=paciente)
    atendimento_evolucao  = Atendimento.objects.filter(paciente=paciente,tipo='EV').count()
    atendimento_avaliacao = Atendimento.objects.filter(paciente=paciente,tipo='AV').count()
    guias = Guia.objects.filter(paciente=paciente).order_by('-validade')
    contas= ContaReceber.objects.filter(paciente=paciente).order_by('-data')
    context = {
        'profissional':profissional,
        'atendimentos':atendimentos,
        'evolucao':atendimento_evolucao,
        'avaliacao':atendimento_avaliacao,
        'paciente':paciente,
        'agendamentos':agendamentos_count,
        'agendamentos_DM_count':agendamentos_DM_count,
        'agendamentos_CC_count':agendamentos_CC_count,
        'guias':guias,
        'contas':contas,
    }
    return render(request,'historico.html',context)