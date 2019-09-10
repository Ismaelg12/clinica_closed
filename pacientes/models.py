# -*- coding: utf-8 -*-
from django.db import models
from core.utils import SEXO,RACA,ESTADO_CIVIL,UF
from core.models import Convenio
from controle_usuarios.models import Profissional
from django.urls import reverse 
from datetime import datetime


class Paciente(models.Model):
	#informações basicas do paciente
	nome              = models.CharField('Nome',max_length=60)
	pai               = models.CharField(max_length=60,blank=True)
	mae               = models.CharField(max_length=60,blank=True)
	data_nascimento   = models.DateField(blank=True,null=True)
	sexo              = models.CharField('Sexo', max_length=1, choices=SEXO, blank=True)
	cpf               = models.CharField(max_length=14,unique=True,blank=True,null=True)
	rg                = models.CharField(max_length=14,blank=True,null=True)
	uf                = models.CharField(max_length=2,choices=UF,default='PI')
	#endereco
	cidade            = models.CharField('Cidade', max_length=40,blank=True)
	rua               = models.CharField('Rua', max_length=70,blank=True)
	bairro            = models.CharField('Bairro',max_length=70,blank=True)
	complemento       = models.CharField(max_length=70,blank=True)
	cep               = models.CharField('CEP',max_length=12, blank=True)
	email             = models.EmailField('E-mail', max_length=70,blank=True,null=True)
	telefone          = models.CharField('Telefone Principal',max_length=20)
	telefone_fixo     = models.CharField('Telefone Fixo',max_length=20,blank=True)
	#complemento
	#profissional      = models.ForeignKey(Profissional ,on_delete=models.SET_NULL,null=True)
	profissional      = models.ManyToManyField(Profissional)
	raca              = models.CharField(max_length=1,choices=RACA,blank=True)
	estado_civil      = models.CharField(choices=ESTADO_CIVIL,max_length=1,blank=True)
	profissao         = models.CharField(max_length=50,blank=True)
	#convenios
	convenio          = models.ForeignKey(Convenio,on_delete=models.SET_NULL,null=True,blank=True)
	num_convenio      = models.CharField('Nº da Carteira',max_length=17,blank=True)
	validade_carteira = models.DateField('Validade Carteira',blank=True,null=True)	
	observacao        = models.TextField(max_length=500,blank=True)
	atualizado_em     = models.DateTimeField('Atualizado em', auto_now=True)
	criado_em         = models.DateTimeField('Criado em', auto_now_add=True)


	class Meta:
		verbose_name = 'paciente'
		verbose_name_plural = 'pacientes'
		ordering = ['nome']
		
	def __str__(self):
		return self.nome
		
	def idade(self):
		return int((datetime.now().date()-self.data_nascimento).days/365.25)
