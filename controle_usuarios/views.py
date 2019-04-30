# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from controle_usuarios.models import Profissional
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import ProtectedError
from django.contrib import messages
from atendimento.models import Agendamento
from controle_usuarios.forms import ProfissinalForm
from django.contrib.auth.decorators import login_required

'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           Views de Usuarios
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

#redireciona dependendo do tipo de usuario
@login_required
def login_success(request):
    if request.user.is_superuser:
        # user is an admin redirect to dashboard
        messages.success(request,"Bem Vindo ao Sistema!!")
        return redirect('home')
    else:
        usuario = request.user.pk
        atendente = Profissional.objects.filter(user=usuario,tipo=1)
        #print(atendente)
        p = Profissional.objects.filter(user=usuario,tipo=2)
        #print(p)
        if p:
            # user is an Profissional redirect to agendamentos
            messages.success(request,"Bem Vindo ao Sistema!!")
            return redirect('agendamentos')
        else:
            # user is an atendente redirect to Home
            messages.success(request,"Bem Vindo ao Sistema!!")
            return redirect('home')
            
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           Crud de Profissional/Usuarios
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''
@login_required
def profissionais(request):
    prof = Profissional.objects.all().exclude(user__username='admin')
    context = {
        'lista_profissionais':prof,
    }
    return render(request,'profissionais/profissionais.html',context)

@login_required
@transaction.atomic
def add_profissional(request):
    user_form = UserCreationForm(request.POST or None)
    profissional_form = ProfissinalForm(request.POST or None)
    if user_form.is_valid() and profissional_form.is_valid():
        user = user_form.save()
        user.refresh_from_db()  # This will load the Profile created by the Signal
        profissional_form = ProfissinalForm(request.POST, instance=user.profissional)  # Reload the profile form with the profile instance
        profissional_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
        profissional_form.save()  # Gracefully save the form
        messages.success(request,'Profissional Cadastrado com Sucesso! ')
        return redirect('home')
    return render(request, 'profissionais/add_profissional.html', {
        'user_form': user_form,
        'profissional_form': profissional_form
    })

@login_required
def profissional_detalhe(request,pk):
    profissional = Profissional.objects.get(pk=pk)
    context = {
        'prof':profissional,
    }
    return render(request,'profissionais/profissional_detalhe.html',context)
    
@login_required   
def update_profissional(request,pk):
    profissional = Profissional.objects.get(pk=pk)
    at                   = Profissional.objects.filter(user=request.user,tipo=1)
    profissionals        = Profissional.objects.filter(user=request.user,tipo=2)
    profissional_form = ProfissinalForm(request.POST or None, instance=profissional)
    if profissional_form.is_valid():
        profissional_form.save()
        messages.success(request, ('Dados atualizados com Sucesso!'))
        return redirect('home')
    return render(request, 'profissionais/edit_profissional.html', {
        'profissional_form': profissional_form,'atend':at,'prof':profissionals
    })


@login_required 
def excluir_profissional(request,pk):
    try :
        profissional = Profissional.objects.get(pk=pk).delete()
        messages.error(request, 'Profissional Deletado Com Sucesso.')
    except ProtectedError:
        messages.warning(request,
         "você não pode deletar esse profissional porque ele atendeu pacientes!!")
    return redirect('profissionais')