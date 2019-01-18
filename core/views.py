# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,CreateView,TemplateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from core.models import Convenio,Sala,Procedimento,ListaEspera
from core.forms import ConvenioForm,SalaForm,ProcedimentoForm,ListaEsperaForm
from core.mixins import DashboardMixin
from django.utils import timezone
from django.contrib import messages
from pacientes.models import Paciente
from atendimento.models import Agendamento
from django.db.models import ProtectedError,Count,Q
from controle_usuarios.models import Profissional
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           Dashboard
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
class DashboardView(TemplateView,DashboardMixin):
    template_name = 'dashboard.html'
    """
    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        #contexto enviado para permmissoes de atendentee profissional
        context['atendente'] = Profissional.objects.filter(
            user=self.request.user,tipo=1
        )
        context['profissional'] = Profissional.objects.filter(
            user=self.request.user,tipo=2
        )
        return context
    """
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                          view de lista de vagas
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
def vagas(request):
    today = datetime.datetime.now()
    profissional = Profissional.objects.annotate(
    number_agenda=Count('agendamento', filter=Q(agendamento__data=today))).filter(tipo=2)
    context = {
        'vagas':profissional,
    }
    return render(request,'vagas.html',context)
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           CRUD Convenios
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
class ConvenioCreateView(LoginRequiredMixin,CreateView):
    model         = Convenio
    template_name = 'convenio/convenio_add.html'
    form_class    = ConvenioForm
    success_url   = reverse_lazy('convenios')

class ConvenioListView(LoginRequiredMixin,ListView):
    model = Convenio
    context_object_name = 'convenios'
    template_name = 'convenio/convenio.html'

class ConvenioUpdateView(LoginRequiredMixin,UpdateView):
    model         = Convenio
    template_name = 'convenio/convenio_add.html'
    form_class    = ConvenioForm
    success_url   = reverse_lazy('convenios')

@login_required 
def ConvenioDeleteView(request,pk):
    try :
        convenio = get_object_or_404(Convenio, pk=pk).delete()
        messages.error(request, 'Convenio Deletado Com Sucesso.')
    except ProtectedError:
        messages.warning(request,
         "Falha ao excluir. Existem atendimentos cadastrados com este convênio.")
    return redirect('convenios')

'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           CRUD Salas
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

class SalaCreateView(LoginRequiredMixin,CreateView):
    model         = Sala
    template_name = 'salas/sala_add.html'
    form_class    = SalaForm
    success_url   = reverse_lazy('salas')

class SalaListView(LoginRequiredMixin,ListView):
    model = Sala
    context_object_name = 'salas'
    template_name = 'salas/salas.html'

class SalaUpdateView(LoginRequiredMixin,UpdateView):
    model         = Sala
    template_name = 'salas/sala_add.html'
    form_class    = SalaForm
    success_url   = reverse_lazy('salas')

class SalaDeleteView(LoginRequiredMixin,DeleteView):
    model         = Sala
    success_url   = reverse_lazy('salas')
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           CRUD Procedimentos
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

class ProcedCreateView(LoginRequiredMixin,CreateView):
    model         = Procedimento
    template_name = 'procedimento/procedimento_add.html'
    form_class    = ProcedimentoForm
    success_url   = reverse_lazy('procedimentos')

class ProcedListView(LoginRequiredMixin,ListView):
    model = Procedimento
    context_object_name = 'procedimentos'
    template_name = 'procedimento/procedimentos.html'

class ProcedUpdateView(LoginRequiredMixin,UpdateView):
    model         = Procedimento
    template_name = 'procedimento/procedimento_add.html'
    form_class    = ProcedimentoForm
    success_url   = reverse_lazy('procedimentos')

@login_required 
def ProcedDeleteView(request,pk):
    try :
        procedimento = get_object_or_404(Procedimento, pk=pk).delete()
        messages.error(request, 'procedimento Deletado Com Sucesso.')
    except ProtectedError:
        messages.warning(request,
         "Falha ao excluir. Existem atendimentos cadastrados com este procedimento.")
    return redirect('procedimentos')


'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           CRUD Lista de Espera
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

class EsperaCreateView(LoginRequiredMixin,CreateView):
    model         = ListaEspera
    template_name = 'lista_de_espera/adicionar.html'
    form_class    = ListaEsperaForm
    success_url   = reverse_lazy('lista_espera')

class EsperaListView(LoginRequiredMixin,ListView):
    model = ListaEspera
    context_object_name = 'lista'
    template_name = 'lista_de_espera/lista.html'

class EsperaUpdateView(LoginRequiredMixin,UpdateView):
    model         = ListaEspera
    template_name = 'lista_de_espera/adicionar.html'
    form_class    = ListaEsperaForm
    success_url   = reverse_lazy('lista_espera')

class EsperaDeleteView(LoginRequiredMixin,DeleteView):
    model         = ListaEspera
    success_url   = reverse_lazy('lista_espera')
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           Aniversariantes
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
@login_required
def aniversarios(request):
    today     = timezone.now().date()
    paciente  = Paciente.objects.filter(data_nascimento__day=today.day,data_nascimento__month=today.month)
    context   = {
        'pacientes':paciente,
    }
    return render(request,'aniversariantes.html',context)