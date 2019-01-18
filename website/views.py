# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from website.forms import contact_form
from django.core.mail import send_mail, BadHeaderError

#form de contato do site
def home(request):
    form = contact_form(request.POST or None)
    if form.is_valid():
        contact_name    = form.cleaned_data['contact_name']
        contact_email   = form.cleaned_data['contact_email']
        contact_phone   = form.cleaned_data['contact_phone']
        contact_message = form.cleaned_data['contact_message']
        try:
            send_mail(contact_name, contact_message, contact_email, ['fisiolifephb@outlook.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('sucesso')
    return render(request,'index.html',{'form':form})

def success(request):
    return HttpResponse(
      '<h3>Enviado com Successo! Obrigado pela sua mensagem.</h3></br> <a href="/">clique aqui e volte para o site</a>'
      )