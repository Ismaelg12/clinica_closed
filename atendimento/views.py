# -*- coding: utf-8 -*-
from django.utils import timezone
#import datetime
from datetime import timedelta, datetime
from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView
from django.template.loader import render_to_string
from atendimento.forms import *
from atendimento.models import Atendimento,Guia,Evolucao
from core.models import Sala,Convenio,Procedimento
from pacientes.models import Paciente
from agenda.models import Agendamento
from controle_usuarios.models import Profissional
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from atendimento.render_pdf import *
from django.db.models import ProtectedError
from django.forms import inlineformset_factory
from django.db.models import Q
from django.core.paginator import Paginator
    
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           Crud de Atendimentos
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
@login_required
def atendimentos(request):
    #variavel para distiguir atendimentos por profissional
    prof = ""
    #variaveis para saber o tipo de usuario logado no template
    pf = Profissional.prof_objects.filter(user=request.user,tipo=2)
    at = Profissional.prof_objects.filter(user=request.user,tipo=1)
    if pf.exists():
        prof = Profissional.prof_objects.get(user=request.user,tipo=2)
    else:
        pass
    if request.GET.get('date_ranger'):
        date_range        = request.GET.get('date_ranger')
        start_date_string = datetime.strptime(date_range.split(' / ')[0],'%d/%m/%Y').strftime('%Y-%m-%d')
        end_date_string   = datetime.strptime(date_range.split(' / ')[1],'%d/%m/%Y').strftime('%Y-%m-%d')
        
        paciente          = request.GET.get('paciente')
        profissional      = request.GET.get('profissional')
        tipo_atendimento  = request.GET.get('tipo')
        

        if prof:
            #se profissional estiver logado ele exibe a busca conforme ele
            if tipo_atendimento != None:
                atendimento = Atendimento.objects.filter(data__range=(start_date_string,end_date_string),
                    profissional_id=prof.id,tipo=tipo_atendimento,paciente__nome__icontains=paciente).values(
                'id','tipo','paciente__nome','data','profissional__nome', 'guia__numero','criado_em')
            else:
                atendimento = Atendimento.objects.filter(data__range=(start_date_string,end_date_string),
                    profissional_id=prof.id,paciente__nome__icontains=paciente).values(
                'id','tipo','paciente__nome','data','profissional__nome', 'guia__numero','criado_em')
        else:
            #se admin estiver logado
            if tipo_atendimento != None:
                atendimento = Atendimento.objects.filter(data__range=(start_date_string,end_date_string),
                    profissional__nome__icontains=profissional,
                    tipo=tipo_atendimento,paciente__nome__icontains=paciente).values(
                'id','tipo','paciente__nome','data','profissional__nome', 'guia__numero','criado_em')
            else:
                atendimento = Atendimento.objects.filter(data__range=(start_date_string,end_date_string),
                    profissional__nome__icontains=profissional,
                    paciente__nome__icontains=paciente).values(
                'id','tipo','paciente__nome','data','profissional__nome', 'guia__numero','criado_em')
    else:
        #exibe todos os atendimentos quando abrir a pagina
        if prof:
            atendimento = Atendimento.objects.filter(profissional_id=prof.id).values(
            'id','tipo','paciente__nome','data','profissional__nome', 'guia__numero','criado_em').order_by('-data')
        else:
            atendimento = Atendimento.objects.all().values(
            'id','tipo','paciente__nome','data','profissional__nome', 'guia__numero','criado_em').order_by('-data')
    context = {
        'pf':pf,
        'at':at,
        'atendimentos':atendimento,
    }
    return render(request,'atendimento/atendimentos.html',context)



#view de adicionar atendimentos
def atendimento_add(request,pk):
    #data para as guias
    data_atual    = datetime.now()
    pf            = Profissional.objects.get(user=request.user)
    agendamento   = get_object_or_404(Agendamento,pk=pk)
    nome_da_ficha = ""
    oculta_fields = ""#apenas para condição em template
    if request.GET.get('tipo') == 'evolucao':
        nome_da_ficha = 'Evolução'
        form_fichas   = EvolucaoForm(request.POST or None)
    elif request.GET.get('tipo') == 'TerapiaOcupacional':
        form_fichas   = TerapiaOcupacionalForm(request.POST or None)
        nome_da_ficha = 'Avaliação Terapia Ocupacional'
    elif request.GET.get('tipo') == 'Psiquiatra':
        form_fichas   = PsiquiatriaForm(request.POST or None)
        nome_da_ficha = 'Avaliação Psiquiatrica'
    elif request.GET.get('tipo') =='Fisioterapeuta':
        form_fichas   = FisioterapiaForm(request.POST or None)
        nome_da_ficha = 'Avaliação Fisioterapia'
    elif request.GET.get('tipo') =='AnamineseAdulto':
        form_fichas   = AnamineseAdultoForm(request.POST or None)
        nome_da_ficha = 'Anaminese Adulto'
    elif request.GET.get('tipo') =='AnamineseCrianca':
        form_fichas   = AnamineseCriancaForm(request.POST or None)
        nome_da_ficha = 'Anaminese Crianca'
    elif request.GET.get('tipo') =='Uroginecologia':
        form_fichas   = UroginecologiaForm(request.POST or None)
        nome_da_ficha = 'Uroginecologia'
    elif request.GET.get('tipo') =='Neurologia':
        form_fichas   = NeurologiaForm(request.POST or None)
        nome_da_ficha = 'Neurologia'
    elif request.GET.get('tipo') =='Nutricao':
        form_fichas   = NutricaoForm(request.POST or None)
        nome_da_ficha = 'Nutricao'

    ##################################################################
    if agendamento.convenio.nome == 'particular':
        #messages.error(request,'Atenção!!! Esse Agendamento é Particular, Informe o Valor:)')

        procedimento = ""
        guia         = ""
        oculta_fields= "oculta_fields"
        #print(agendamento.convenio )
    else:
        if Guia.objects.filter(paciente=agendamento.paciente.id,
        quantidade__gte=1,ativo=True,profissional=pf,validade__gte=data_atual).exists():
            procedimento =""
            guia =""
            """
            procedimento = Procedimento.objects.get(
                id=Guia.objects.get(paciente=agendamento.paciente.id,ativo=True,profissional=pf).procedimento.id)
            guia = Guia.objects.get(paciente=agendamento.paciente.id,ativo=True,profissional=pf)
            """
        else:
            messages.warning(request,'Esse Paciente Não Possui 1 Guia Ativa e portanto está sem Procedimento! ')
            procedimento = ""
            guia         = ""
    #seta os selects ao carrega a pagina
    form_atendimento = AtendimentoForm(request.POST or None,initial={
        'profissional':pf.id,
        'hora_inicio':agendamento.hora_inicio,
        'hora_fim':agendamento.hora_fim,
        'paciente':agendamento.paciente.id,
        'convenio':agendamento.convenio.id,
        #'procedimento':procedimento,
        #'guia':guia,
    })
    
    ##################################################################
    #sobrescreve os dados das querysets
    form_atendimento.fields['profissional'].queryset = Profissional.objects.filter(id=pf.id)
    form_atendimento.fields['paciente'].queryset     = Paciente.objects.filter(id=agendamento.paciente.id)
    form_atendimento.fields['convenio'].queryset     = Convenio.objects.filter(id=agendamento.convenio.id)
    if Guia.objects.filter(paciente=agendamento.paciente.id,quantidade__gte=1,ativo=True,
        profissional=pf,validade__gte=data_atual).exists():
        #verifica se a guia existe e que tem quant. maior que 1 para esse paciente que esta no a atendimento
        #se ela existir ele trás o select setado 
        form_atendimento.fields['profissional'].queryset = Profissional.objects.filter(id=pf.id)
        form_atendimento.fields['guia'].queryset         = Guia.objects.filter(
            paciente=agendamento.paciente.id,ativo=True,quantidade__gte=1,profissional=pf,validade__gte=data_atual)

       
        """
        form_atendimento.fields['guia'].queryset         = Guia.objects.filter(
            paciente=agendamento.paciente.id,ativo=True,profissional=pf)
        form_atendimento.fields['procedimento'].queryset = Procedimento.objects.filter(
                    id=Guia.objects.get(paciente=agendamento.paciente.id,ativo=True,profissional=pf).procedimento.id)
        """
    else:
        #se a guia não existir ele retorna os campos vazios com essa msg
        #messages.warning(request,
        #'Paciente possui 1 GUIA mas não pode ser usada por que está sem sessões e portanto sem Procedimento')
        form_atendimento.fields['procedimento'].queryset = Procedimento.objects.none()
        form_atendimento.fields['guia'].queryset         = Guia.objects.none()
    
    if form_atendimento.is_valid() and form_fichas.is_valid():
        #salva os 2 forms  e os relaciona
        atendimento             = form_atendimento.save(commit=False)
        #print("guia proce",form_atendimento.instance.guia.procedimento)
        if agendamento.convenio.nome != 'particular':
            #pre não da erro de procedimento em branco
            atendimento.procedimento = form_atendimento.instance.guia.procedimento
            atendimento.save()
        else:
            atendimento.save()
        ficha              = form_fichas.save(commit=False)
        ficha.atendimento  = atendimento

        #condição para setar o tipo de atendimento com base no nome da ficha
        if ficha._meta.verbose_name == "Evolução":
            atendimento.tipo = "EV"
        else:
            atendimento.tipo = "AV"
        atendimento.save()
        ficha.save()
        #decrementa a guia e depois salva
        if agendamento.convenio.nome != 'particular':
            atendimento.guia.quantidade -=1
            atendimento.guia.save()
            atendimento.save()
            #finaliza a guia se tiver menor que zero a quantidade
            if atendimento.guia.quantidade < 1:
                atendimento.guia.ativo = False
                atendimento.guia.save()
        #altera o status e depois salva
        agendamento.status = "AT"
        agendamento.save()
        messages.success(request,'Atendimento Adicionado com Sucesso! ')
        return redirect('agendamentos')
    context = {
        'form':form_atendimento,
        'form_fichas':form_fichas,
        'nome_da_ficha':nome_da_ficha,
        'oculta_fields':oculta_fields,
    }
    return render(request,'atendimento/adicionar_atendimento.html',context)

"""
#view antiga de adicionar atendimentos
def atendimento_add(request,pk):
    pf            = Profissional.objects.get(user=request.user)
    agendamento   = get_object_or_404(Agendamento,pk=pk)
    nome_da_ficha = ""
    oculta_fields = ""#apenas para condição em template
    if request.GET.get('tipo') == 'evolucao':
        nome_da_ficha = 'Evolução'
        form_fichas   = EvolucaoForm(request.POST or None)
    elif request.GET.get('tipo') == 'TerapiaOcupacional':
        form_fichas   = TerapiaOcupacionalForm(request.POST or None)
        nome_da_ficha = 'Avaliação Terapia Ocupacional'
    elif request.GET.get('tipo') == 'Psiquiatra':
        form_fichas   = PsiquiatriaForm(request.POST or None)
        nome_da_ficha = 'Avaliação Psiquiatrica'
    elif request.GET.get('tipo') =='Fisioterapeuta':
        form_fichas   = FisioterapiaForm(request.POST or None)
        nome_da_ficha = 'Avaliação Fisioterapia'
    elif request.GET.get('tipo') =='AnamineseAdulto':
        form_fichas   = AnamineseAdultoForm(request.POST or None)
        nome_da_ficha = 'Anaminese Adulto'
    elif request.GET.get('tipo') =='AnamineseCrianca':
        form_fichas   = AnamineseCriancaForm(request.POST or None)
        nome_da_ficha = 'Anaminese Crianca'
    elif request.GET.get('tipo') =='Uroginecologia':
        form_fichas   = UroginecologiaForm(request.POST or None)
        nome_da_ficha = 'Uroginecologia'
    elif request.GET.get('tipo') =='Neurologia':
        form_fichas   = NeurologiaForm(request.POST or None)
        nome_da_ficha = 'Neurologia'
    elif request.GET.get('tipo') =='Nutricao':
        form_fichas   = NutricaoForm(request.POST or None)
        nome_da_ficha = 'Nutricao'

    ##################################################################
    if agendamento.convenio.nome == 'particular':
        #messages.error(request,'Atenção!!! Esse Agendamento é Particular, Informe o Valor:)')

        procedimento = ""
        guia         = ""
        oculta_fields= "oculta_fields"
        #print(agendamento.convenio )
    else:
        if Guia.objects.filter(paciente=agendamento.paciente.id,
        quantidade__gte=1,ativo=True,profissional=pf).exists():
            procedimento = Procedimento.objects.get(
                id=Guia.objects.get(paciente=agendamento.paciente.id,ativo=True,profissional=pf).procedimento.id)
            guia = Guia.objects.get(paciente=agendamento.paciente.id,ativo=True,profissional=pf)
        else:
            messages.warning(request,'Esse Paciente Não Possui 1 Guia Ativa e portanto está sem Procedimento! ')
            procedimento = ""
            guia         = ""
    #seta os selects ao carrega a pagina
    form_atendimento = AtendimentoForm(request.POST or None,initial={
        'profissional':pf.id,
        'hora_inicio':agendamento.hora_inicio,
        'hora_fim':agendamento.hora_fim,
        'paciente':agendamento.paciente.id,
        'convenio':agendamento.convenio.id,
        'procedimento':procedimento,
        'guia':guia,
    })
    
    ##################################################################
    #sobrescreve os dados das querysets
    form_atendimento.fields['profissional'].queryset = Profissional.objects.filter(id=pf.id)
    form_atendimento.fields['paciente'].queryset     = Paciente.objects.filter(id=agendamento.paciente.id)
    form_atendimento.fields['convenio'].queryset     = Convenio.objects.filter(id=agendamento.convenio.id)
    if Guia.objects.filter(paciente=agendamento.paciente.id,quantidade__gte=1,ativo=True,profissional=pf).exists():
        #verifica se a guia existe e que tem quant. maior que 1 para esse paciente que esta no a atendimento
        #se ela existir ele trás o select setado 
        form_atendimento.fields['profissional'].queryset = Profissional.objects.filter(id=pf.id)

        form_atendimento.fields['guia'].queryset         = Guia.objects.filter(
            paciente=agendamento.paciente.id,ativo=True,profissional=pf)
        form_atendimento.fields['procedimento'].queryset = Procedimento.objects.filter(
                    id=Guia.objects.get(paciente=agendamento.paciente.id,ativo=True,profissional=pf).procedimento.id)
    else:
        #se a guia não existir ele retorna os campos vazios com essa msg
        #messages.warning(request,
            #'Paciente possui 1 GUIA mas não pode ser usada por que está sem sessões e portanto sem Procedimento')
        form_atendimento.fields['procedimento'].queryset = Procedimento.objects.none()
        form_atendimento.fields['guia'].queryset = Guia.objects.none()
    
    if form_atendimento.is_valid() and form_fichas.is_valid():
        #salva os 2 forms  e os relaciona
        atendimento        = form_atendimento.save()
        ficha              = form_fichas.save(commit=False)
        ficha.atendimento  = atendimento
        #condição para setar o tipo de atendimento com base no nome da ficha
        if ficha._meta.verbose_name == "Evolução":
            atendimento.tipo = "EV"
        else:
            atendimento.tipo = "AV"
        atendimento.save()
        ficha.save()
        #decrementa a guia e depois salva
        if agendamento.convenio.nome != 'particular':
            atendimento.guia.quantidade -=1
            atendimento.guia.save()
            atendimento.save()
        #altera o status e depois salva
        agendamento.status = "AT"
        agendamento.save()
        messages.success(request,'Atendimento Adicionado com Sucesso! ')
        return redirect('agendamentos')
    context = {
        'form':form_atendimento,
        'form_fichas':form_fichas,
        'nome_da_ficha':nome_da_ficha,
        'oculta_fields':oculta_fields,
    }
    return render(request,'atendimento/adicionar_atendimento.html',context)
"""

@login_required
def atendimento_update(request,pk):
    pf               = Profissional.objects.get(user=request.user)
    atendimento      = get_object_or_404(Atendimento,pk=pk)
    form_atendimento = AtendimentoForm(request.POST or None,instance = atendimento)
    form_ficha       = ""
    nome_da_ficha    = ""
    exibe_botao      =""
    if request.GET.get('ocultarBotao') == 'ocultarBotao':
        exibe_botao = "display_button"
        
        #exibe_botao_salvar = True
    #condição para trazer a ficha correta para atualizar
    if Evolucao.objects.filter(atendimento=atendimento.id).exists():
        ficha      = Evolucao.objects.get(atendimento=atendimento.id)
        form_ficha = EvolucaoForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Evolução'
    elif TerapiaOcupacional.objects.filter(atendimento=atendimento.id).exists():
        ficha         = TerapiaOcupacional.objects.get(atendimento=atendimento.id)
        form_ficha    = TerapiaOcupacionalForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Avaliação Terapia Ocupacional'
    elif Psiquiatria.objects.filter(atendimento=atendimento.id).exists():
        ficha         = Psiquiatria.objects.get(atendimento=atendimento.id)
        form_ficha    = PsiquiatriaForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Avaliação Psiquiatrica'
    elif Fisioterapeuta.objects.filter(atendimento=atendimento.id).exists():
        ficha         = Fisioterapeuta.objects.get(atendimento=atendimento.id)
        form_ficha    = FisioterapiaForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Avaliação Fisioterapia'
    elif Anaminese_adulto.objects.filter(atendimento=atendimento.id).exists():
        ficha         = Anaminese_adulto.objects.get(atendimento=atendimento.id)
        form_ficha    = AnamineseAdultoForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Anaminese Adulto'
    elif Anaminese_crianca.objects.filter(atendimento=atendimento.id).exists():
        ficha         = Anaminese_crianca.objects.get(atendimento=atendimento.id)
        form_ficha    = AnamineseCriancaForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Anaminese Crianca'
    elif Uroginecologia.objects.filter(atendimento=atendimento.id).exists():
        ficha         = Uroginecologia.objects.get(atendimento=atendimento.id)
        form_ficha    = UroginecologiaForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Uroginecologia'
    elif Neurologia.objects.filter(atendimento=atendimento.id).exists():
        ficha         = Neurologia.objects.get(atendimento=atendimento.id)
        form_ficha    = NeurologiaForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Neurologia'
    elif Nutricao.objects.filter(atendimento=atendimento.id).exists():
        ficha         = Nutricao.objects.get(atendimento=atendimento.id)
        form_ficha    = NutricaoForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Nutricao'
    ##################################################################
    #sobrescreve os dados das querysets
    if request.user.is_superuser:
        form_atendimento.fields['profissional'].queryset = Profissional.objects.filter(id=atendimento.profissional.id)
    else:
        form_atendimento.fields['profissional'].queryset = Profissional.objects.filter(id=pf.id)

    form_atendimento.fields['paciente'].queryset     = Paciente.objects.filter(id=atendimento.paciente.id)
    form_atendimento.fields['convenio'].queryset     = Convenio.objects.filter(id=atendimento.convenio.id)
    """
    if Guia.objects.filter(paciente=atendimento.paciente.id,quantidade__gte=1,ativo=True).exists():
        #verifica se a guia existe e que tem quant. maior que 1 para esse paciente que esta no a atendimento
        #se ela existir ele trás o select setado 
        form_atendimento.fields['profissional'].queryset = Profissional.objects.filter(id=pf.id)

        form_atendimento.fields['guia'].queryset         = Guia.objects.filter(
            paciente=atendimento.paciente.id,ativo=True)
        form_atendimento.fields['procedimento'].queryset = Procedimento.objects.filter(
                    id=Guia.objects.get(paciente=atendimento.paciente.id,ativo=True).procedimento.id)
    else:
        #se a guia não existir ele retorna os campos vazios com essa msg
        #messages.warning(request,
            #'Paciente possui 1 GUIA mas não pode ser usada por que está sem sessões e portanto sem Procedimento')
        form_atendimento.fields['procedimento'].queryset = Procedimento.objects.none()
        form_atendimento.fields['guia'].queryset = Guia.objects.none()
    """
    if form_atendimento.is_valid() and form_ficha.is_valid():
        form_ficha.save()
        form_atendimento.save()
        messages.success(request,'Atendimento Atualizado com Sucesso! ')
        return redirect('atendimentos')
    context = {
        'form':form_atendimento,
        'form_fichas':form_ficha,
        'nome_da_ficha':nome_da_ficha,
        'ocultar_botao_salvar':exibe_botao,
    }
    return render(request,'atendimento/update_atendimento.html',context)


"""
view antiga de update
@login_required
def atendimento_update(request,pk):
    pf               = Profissional.objects.get(user=request.user)
    atendimento      = get_object_or_404(Atendimento,pk=pk)
    form_atendimento = AtendimentoForm(request.POST or None,instance = atendimento)
    form_ficha       = ""
    nome_da_ficha    = ""
    exibe_botao      =""
    if request.GET.get('ocultarBotao') == 'ocultarBotao':
        exibe_botao = "display_button"
        
        #exibe_botao_salvar = True
    #condição para trazer a ficha correta para atualizar
    if Evolucao.objects.filter(atendimento=atendimento.id).exists():
        ficha      = Evolucao.objects.get(atendimento=atendimento.id)
        form_ficha = EvolucaoForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Evolução'
    elif TerapiaOcupacional.objects.filter(atendimento=atendimento.id).exists():
        ficha         = TerapiaOcupacional.objects.get(atendimento=atendimento.id)
        form_ficha    = TerapiaOcupacionalForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Avaliação Terapia Ocupacional'
    elif Psiquiatria.objects.filter(atendimento=atendimento.id).exists():
        ficha         = Psiquiatria.objects.get(atendimento=atendimento.id)
        form_ficha    = PsiquiatriaForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Avaliação Psiquiatrica'
    elif Fisioterapeuta.objects.filter(atendimento=atendimento.id).exists():
        ficha         = Fisioterapeuta.objects.get(atendimento=atendimento.id)
        form_ficha    = FisioterapiaForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Avaliação Fisioterapia'
    elif Anaminese_adulto.objects.filter(atendimento=atendimento.id).exists():
        ficha         = Anaminese_adulto.objects.get(atendimento=atendimento.id)
        form_ficha    = AnamineseAdultoForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Anaminese Adulto'
    elif Anaminese_crianca.objects.filter(atendimento=atendimento.id).exists():
        ficha         = Anaminese_crianca.objects.get(atendimento=atendimento.id)
        form_ficha    = AnamineseCriancaForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Anaminese Crianca'
    elif Uroginecologia.objects.filter(atendimento=atendimento.id).exists():
        ficha         = Uroginecologia.objects.get(atendimento=atendimento.id)
        form_ficha    = UroginecologiaForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Uroginecologia'
    elif Neurologia.objects.filter(atendimento=atendimento.id).exists():
        ficha         = Neurologia.objects.get(atendimento=atendimento.id)
        form_ficha    = NeurologiaForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Neurologia'
    elif Nutricao.objects.filter(atendimento=atendimento.id).exists():
        ficha         = Nutricao.objects.get(atendimento=atendimento.id)
        form_ficha    = NutricaoForm(request.POST or None,instance=ficha)
        nome_da_ficha = 'Nutricao'
    ##################################################################
    #sobrescreve os dados das querysets
    if request.user.is_superuser:
        form_atendimento.fields['profissional'].queryset = Profissional.objects.filter(id=atendimento.profissional.id)
    else:
        form_atendimento.fields['profissional'].queryset = Profissional.objects.filter(id=pf.id)

    form_atendimento.fields['paciente'].queryset     = Paciente.objects.filter(id=atendimento.paciente.id)
    form_atendimento.fields['convenio'].queryset     = Convenio.objects.filter(id=atendimento.convenio.id)
    if Guia.objects.filter(paciente=atendimento.paciente.id,quantidade__gte=1,ativo=True).exists():
        #verifica se a guia existe e que tem quant. maior que 1 para esse paciente que esta no a atendimento
        #se ela existir ele trás o select setado 
        form_atendimento.fields['profissional'].queryset = Profissional.objects.filter(id=pf.id)

        form_atendimento.fields['guia'].queryset         = Guia.objects.filter(
            paciente=atendimento.paciente.id,ativo=True)
        form_atendimento.fields['procedimento'].queryset = Procedimento.objects.filter(
                    id=Guia.objects.get(paciente=atendimento.paciente.id,ativo=True).procedimento.id)
    else:
        #se a guia não existir ele retorna os campos vazios com essa msg
        #messages.warning(request,
            #'Paciente possui 1 GUIA mas não pode ser usada por que está sem sessões e portanto sem Procedimento')
        form_atendimento.fields['procedimento'].queryset = Procedimento.objects.none()
        form_atendimento.fields['guia'].queryset = Guia.objects.none()
        
    if form_atendimento.is_valid() and form_ficha.is_valid():
        form_ficha.save()
        form_atendimento.save()
        messages.success(request,'Atendimento Atualizado com Sucesso! ')
        return redirect('atendimentos')
    context = {
        'form':form_atendimento,
        'form_fichas':form_ficha,
        'nome_da_ficha':nome_da_ficha,
        #'ocultar_botao_salvar':exibe_botao,
    }
    return render(request,'atendimento/adicionar_atendimento.html',context)

"""
@login_required
def excluir_atendimento(request,pk):
    atendimento = get_object_or_404(Atendimento,pk=pk)
    atendimento.delete()
    messages.success(request,'Excluido com Sucesso! ')
    return redirect('atendimentos')


@login_required
def finalizar_guia(request,pk):
    guia = get_object_or_404(Guia,pk=pk)
    guia.ativo = "False"
    guia.save()
    messages.success(request,'Guia Finalizada com Sucesso! ')
    return redirect('guias')

""" 
@login_required
def atendimento_detalhe(request,pk):
    atendimento = get_object_or_404(Atendimento,pk=pk)
    return render(request,'atendimento/atendimento_detalhe.html',{'atendimento':atendimento})
"""

@login_required
def load_procedimentos_guias(request):
    #carrega os procedimentos conforme o convenio em add guias
    today = timezone.now()
    convenio_id   = request.GET.get('convenio')
    #paciente_id   = request.GET.get('paciente')
    #guias         = Guia.objects.get(paciente=paciente_id,validade__gte=today,quantidade__gte=1)
    guias = ""
    procedimentos = Procedimento.objects.filter(convenio=convenio_id).order_by('nome')
    context = {
        'procedimentos': procedimentos,
        'guias': guias
    }
    return render(request, 'atendimento/procedimentos.html',context)

'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           CRUD Guias
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

"""
@login_required
def guias(request):
    guia       = Guia.objects.filter(ativo=True)
    paginator  = Paginator(guia,50) # Show 25 contacts per page
    page       = request.GET.get('page')
    guia_pages = paginator.get_page(page)
    if  request.method == 'GET':
        profissional_search = request.GET.get('profissional')
        numero              = request.GET.get('numero')
        paciente            = request.GET.get('paciente')
        #print('result',profissional_search,numero,paciente)
        if numero:
            guia_pages          = Guia.objects.filter(
            numero__icontains=numero)
        elif paciente:
            guia_pages          = Guia.objects.filter(
            paciente__nome__icontains=paciente)

        elif profissional_search:
            guia_pages          = Guia.objects.filter(
            profissional__nome__icontains=profissional_search)
        
    return render(request,'guias/guias.html',{'guias':guia_pages})
"""

class GuiaListView(LoginRequiredMixin,ListView):
    model               =  Guia
    template_name       = 'guias/guias.html'
    context_object_name = 'guias'
    paginate_by = 50
    
    def get_queryset(self, **kwargs):
        pf = Profissional.objects.filter(
            user=self.request.user,tipo=2)
        profissional_search = self.request.GET.get('profissional')
        numero              = self.request.GET.get('numero')
        paciente            = self.request.GET.get('paciente')
        if pf.exists():
            prof = Profissional.prof_objects.get(user=self.request.user,tipo=2)
            queryset = Guia.objects.filter(ativo=True,profissional=prof.id)
        else:
            queryset = Guia.objects.filter(ativo=True)
        if pf.exists():
            #if profissinal estiver logado so mostra os agendamento dele
            prof = Profissional.prof_objects.get(user=self.request.user,tipo=2)
            if  self.request.method == 'GET':
                if numero:
                    queryset          = Guia.objects.filter(
                    numero__icontains=numero,profissional=prof.id)
                elif paciente:
                    queryset          = Guia.objects.filter(
                    paciente__nome__icontains=paciente,profissional=prof.id)
        else:
            #if admin ou atendente estiver logado so mostra tudo
            if  self.request.method == 'GET':
                if numero:
                    queryset          = Guia.objects.filter(
                    numero__icontains=numero)
                elif paciente:
                    queryset          = Guia.objects.filter(
                    paciente__nome__icontains=paciente)

                elif profissional_search:
                    queryset          = Guia.objects.filter(
                    profissional__nome__icontains=profissional_search)
        return queryset
        

    """
    def get_context_data(self, *args, **kwargs):
        context = super(GuiaListView, self).get_context_data(*args, **kwargs)
        context['profissional_logado'] = Profissional.objects.filter(
            user=self.request.user,tipo=2
        )
        context['guias_do_profissional'] = Guia.objects.filter(
               profissional__user=self.request.user)
        #if tiver busca ele filtra os meus pacientes
        if  self.request.method == 'GET':
            profissional_search = self.request.GET.get('profissional')
            numero              = self.request.GET.get('numero')
            paciente            = self.request.GET.get('paciente')
            if numero:
                context['guias_do_profissional']          = Guia.objects.filter(
                numero__icontains=numero,profissional__user=self.request.user)
            elif paciente:
                context['guias_do_profissional']          = Guia.objects.filter(
                paciente__nome__icontains=paciente,profissional__user=self.request.user)
        return context
    """

@login_required
def guias_finalizadas(request):
    guia       = Guia.objects.filter(ativo=False)
    paginator  = Paginator(guia,50) # Show 25 contacts per page
    page       = request.GET.get('page')
    guia_pages = paginator.get_page(page)
    if  request.method == 'GET':
        profissional_search = request.GET.get('profissional')
        numero              = request.GET.get('numero')
        paciente            = request.GET.get('paciente')
        #print('result',profissional_search,numero,paciente)
        if numero:
            guia_pages          = Guia.objects.filter(
            numero__icontains=numero)
        elif paciente:
            guia_pages          = Guia.objects.filter(
            paciente__nome__icontains=paciente)

        elif profissional_search:
            guia_pages          = Guia.objects.filter(
            profissional__nome__icontains=profissional_search)
        
    return render(request,'guias/guias_finalizadas.html',{'guias':guia_pages})

@login_required
def adicionar_guia(request):
    form = GuiaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request,'Guia Adicionada com Sucesso! ')
        return redirect('guias')
    return render(request,'guias/adicionar_guia.html',{'form':form})

@login_required
def update_guia(request,pk):
    guia = Guia.objects.get(pk=pk)
    form = GuiaForm(request.POST or None, instance=guia)
    if form.is_valid():
        form.save()
        messages.success(request,'Guia Atualizada com Sucesso! ')
        return redirect('guias')
    context = {'form':form,'guia':guia}
    return render(request,'guias/update_guia.html',context)

@login_required
def sobre_guia(request,pk):
    guia = Guia.objects.get(pk=pk)
    
    context = {'guia':guia}
    return render(request,'guias/sobre_guia.html',context)

def validar_guia(request,pk):
    guia = Guia.objects.get(pk=pk)
    #form = GuiaForm(request.POST or None, instance=guia)
    if request.method =='POST':
        nova_data = datetime.strptime(request.POST.get(
            'validade').split(' / ')[0],'%d/%m/%Y').strftime('%Y-%m-%d')
        if guia.validada == False:
            guia.validada = True
            guia.validade = nova_data
            guia.save()
            messages.success(request,'Guia Revalidada com Sucesso! ')
            return redirect('guias')
        else:
            messages.success(request,'Atenção!!!! Essa Guia Já foi Revalidada 1 Vez!')
    return render(request,'guias/validar_guia.html',{'guia':guia})


@login_required
def excluir_guia(request,pk):
    try:
        guia = get_object_or_404(Guia,pk=pk)
        guia.delete()
        messages.success(request,'Guia Excluida com Sucesso! ')
    except ProtectedError:
        messages.warning(request,
         "você não pode deletar essa guia porque ele tem atendimentos vinculados a ela!")
    return redirect('guias')