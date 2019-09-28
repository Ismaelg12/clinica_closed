# -*- coding: utf-8 -*-
import datetime
from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView,CreateView,TemplateView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from core.models import Convenio,Sala,Procedimento,ListaEspera,Convenio
from core.forms import ConvenioForm,SalaForm,ProcedimentoForm,ListaEsperaForm
from core.mixins import DashboardMixin
from django.utils import timezone
from django.contrib import messages
from pacientes.models import Paciente
from atendimento.models import Guia
from core.models import Clinica
from django.db.models import ProtectedError,Count,Q
from controle_usuarios.models import Profissional
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from core.decorators import staff_member_required


'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           Dashboard
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''


class DashboardView(TemplateView,DashboardMixin):
    template_name = 'dashboard.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(DashboardView, self).get_context_data(*args, **kwargs)
        #contexto enviado para permmissoes de atendentee profissional
        """
        context['atendente'] = Profissional.objects.filter(
            user=self.request.user,tipo=1
        )
        """
        
        context['clinica']          = Clinica.objects.all()[:1]
        context['convenios']        = Convenio.objects.all()
        context['guia_notificacao'] = Guia.objects.filter(quantidade__lte=2)[:5]
        
        return context
    
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                          view de lista de vagas
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
def vagas(request):
    lista_pf = Profissional.objects.filter(tipo=2)
    start_date = None
    date_now   = None
    if request.GET.get('date_now'):
        date_now   = request.GET.get('date_now')
        start_date = datetime.datetime.strptime(date_now,'%d/%m/%Y').strftime('%Y-%m-%d')
        prof       = request.GET.get('profissional')
        #atendimento = Atendimento.objects.filter(data=(start_date_string),profissional__nome__icontains=profissional,tipo=tipo_atendimento)
        print(date_now)
        profissional_vaga = Profissional.objects.annotate(
        number_agenda=Count('agendamento', filter=Q(agendamento__data=start_date))).filter(tipo=2,nome__icontains=prof)
    else:
        today = datetime.datetime.now()
        profissional_vaga = Profissional.objects.annotate(
        number_agenda=Count('agendamento', filter=Q(agendamento__data=today))).filter(tipo=2)
    context = {
        'vagas':profissional_vaga,
        'lista_pf':lista_pf,
        'date_now':date_now
    }
    return render(request,'vagas.html',context)
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           CRUD Convenios
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
@method_decorator(staff_member_required, name='dispatch')
class ConvenioCreateView(LoginRequiredMixin,CreateView):
    model         = Convenio
    template_name = 'convenio/convenio_add.html'
    form_class    = ConvenioForm
    success_url   = reverse_lazy('convenios')

@method_decorator(staff_member_required, name='dispatch')
class ConvenioListView(LoginRequiredMixin,ListView):
    model               = Convenio
    context_object_name = 'convenios'
    template_name       = 'convenio/convenio.html'

@method_decorator(staff_member_required, name='dispatch')
class ConvenioDetailView(LoginRequiredMixin,DetailView):
    model               = Convenio
    context_object_name = 'convenio'
    template_name       = 'convenio/convenio_detalhe.html'

@method_decorator(staff_member_required, name='dispatch')
class ConvenioUpdateView(LoginRequiredMixin,UpdateView):
    model         = Convenio
    template_name = 'convenio/convenio_add.html'
    form_class    = ConvenioForm
    success_url   = reverse_lazy('convenios')

@login_required 
def ConvenioDeleteView(request,pk):
    try :
        convenio = get_object_or_404(Convenio, pk=pk).delete()
        messages.info(request, 'Convenio Deletado Com Sucesso.')
    except ProtectedError:
        messages.error(request,
         "Falha ao excluir. Existem atendimentos cadastrados com este convênio.")
    return redirect('convenios')

'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           CRUD Salas
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

@method_decorator(staff_member_required, name='dispatch')
class SalaCreateView(LoginRequiredMixin,CreateView):
    model         = Sala
    template_name = 'salas/sala_add.html'
    form_class    = SalaForm
    success_url   = reverse_lazy('salas')

@method_decorator(staff_member_required, name='dispatch')
class SalaListView(LoginRequiredMixin,ListView):
    model = Sala
    context_object_name = 'salas'
    template_name = 'salas/salas.html'

@method_decorator(staff_member_required, name='dispatch')
class SalaUpdateView(LoginRequiredMixin,UpdateView):
    model         = Sala
    template_name = 'salas/sala_add.html'
    form_class    = SalaForm
    success_url   = reverse_lazy('salas')

@method_decorator(staff_member_required, name='dispatch')
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

@method_decorator(staff_member_required, name='dispatch')
class ProcedCreateView(LoginRequiredMixin,CreateView):
    model         = Procedimento
    template_name = 'procedimento/procedimento_add.html'
    form_class    = ProcedimentoForm
    success_url   = reverse_lazy('procedimentos')

#@method_decorator(staff_member_required, name='dispatch')
class ProcedListView(LoginRequiredMixin,ListView):
    model = Procedimento
    context_object_name = 'procedimentos'
    template_name = 'procedimento/procedimentos.html'

@method_decorator(staff_member_required, name='dispatch')
class ProcedUpdateView(LoginRequiredMixin,UpdateView):
    model         = Procedimento
    template_name = 'procedimento/procedimento_add.html'
    form_class    = ProcedimentoForm
    success_url   = reverse_lazy('procedimentos')

@method_decorator(staff_member_required, name='dispatch')
@login_required 
def ProcedDeleteView(request,pk):
    try :
        procedimento = get_object_or_404(Procedimento, pk=pk).delete()
        messages.info(request, 'procedimento Deletado Com Sucesso.')
    except ProtectedError:
        messages.warning(request,
         "Falha ao excluir. Existem atendimentos cadastrados com este procedimento.")
    return redirect('procedimentos')


'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           CRUD Lista de Espera
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
#view que migra o cadastro na lista de espera paera o cadastro de pacientes
def migrar_paciente(request,pk):
    lista_espera = ListaEspera.objects.get(pk=pk)
    Paciente.objects.create(
        nome=lista_espera.nome,
        data_nascimento=lista_espera.data_nascimento,
        sexo=lista_espera.sexo,
    ).save()
    lista_espera.delete()
    messages.success(request,'Cadastro Migrado com Sucesso, Apenas Complete os dados ! ')
    return redirect('lista_espera')


class EsperaCreateView(LoginRequiredMixin,CreateView):
    model         = ListaEspera
    template_name = 'lista_de_espera/adicionar.html'
    form_class    = ListaEsperaForm
    success_url   = reverse_lazy('lista_espera')


class EsperaListView(LoginRequiredMixin,ListView):
    model         = ListaEspera
    template_name = 'lista_de_espera/lista.html'
    
    def get_context_data(self, **kwargs):
        #pf é querysets para exibir profissionais no template para o filtro
        pf            = Profissional.objects.filter(tipo=2,user=self.request.user,)
        context = super(EsperaListView, self).get_context_data(**kwargs)
        if pf.exists():
            context['lista'] = ListaEspera.objects.filter(profissional__user=self.request.user)
        else:
            context['lista'] = ListaEspera.objects.all()
        return context

class EsperaUpdateView(LoginRequiredMixin,UpdateView):
    model         = ListaEspera
    template_name = 'lista_de_espera/adicionar.html'
    form_class    = ListaEsperaForm
    success_url   = reverse_lazy('lista_espera')


class EsperaDetailView(LoginRequiredMixin,DetailView):
    model = ListaEspera
    template_name = 'lista_de_espera/lista_detalhe.html'
    context_object_name = 'espera'


class EsperaDeleteView(LoginRequiredMixin,DeleteView):
    model         = ListaEspera
    success_url   = reverse_lazy('lista_espera')
    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

@login_required
def load_profissional(request):
    especialidade_id = request.GET.get('especialidade')
    pf            = Profissional.prof_objects.filter(area_atuacao=especialidade_id)
    context = {
        'profissionais': pf
    }
    return render(request, 'lista_de_espera/profissionais.html',context)
    
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