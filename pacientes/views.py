# -*- coding: utf-8 -*-
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from pacientes.models import Paciente
from atendimento.models import Atendimento,Agendamento
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

"""
class PacienteDeleteView(LoginRequiredMixin,DeleteView):
    model         = Paciente
    success_url   = reverse_lazy('lista_pacientes')
    error_url = reverse_lazy('atendimentos')
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
    
    def get_error_url(self):
        if self.error_url:
            return self.error_url.format(**self.object.__dict__)
        else:
            raise ImproperlyConfigured(
               "No error URL to redirect to. Provide a error_url.")

    def delete(self, request, *args, **kwargs):
       self.object = self.get_object()
       success_url = self.get_success_url()
       error_url = self.get_error_url()
       try:
            self.object.delete()
            return HttpResponseRedirect(success_url)
       except models.ProtectedError:
            return HttpResponseRedirect(error_url)    
"""

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
    paciente = get_object_or_404(Paciente,pk=pk)
    agendamentos_count = Agendamento.objects.filter(paciente=paciente)
    atendimentos = Atendimento.objects.filter(paciente=paciente)
    atendimento_evolucao = Atendimento.objects.filter(paciente=paciente,tipo='EV')
    atendimento_avaliacao = Atendimento.objects.filter(paciente=paciente,tipo='AV').count()
    context = {
        'atendimentos':atendimentos,
        'evolucao':atendimento_evolucao,
        'avaliacao':atendimento_avaliacao,
        'paciente':paciente,
        'agendamentos':agendamentos_count,
    }
    return render(request,'historico.html',context)