# -*- coding: utf-8 -*-
from django.db import models
from core.utils import SEXO,RACA,ESTADO_CIVIL,UF
from core.models import Convenio

class Paciente(models.Model):
	#informações basicas
	nome            = models.CharField(max_length=40)
	data_nascimento = models.DateField()
	sexo            = models.CharField('Sexo', max_length=1, choices=SEXO, blank=True)
	cpf             = models.CharField(max_length=14,unique=True)
	rg              = models.CharField(max_length=9)
	uf              = models.CharField(max_length=2,choices=UF,default='PI')
	#endereco
	cidade          = models.CharField('Cidade', max_length=40)
	rua             = models.CharField('Rua', max_length=70)
	bairro          = models.CharField('Bairro',max_length=70, blank=True, null=True)
	complemento     = models.CharField(max_length=70,blank=True)
	cep             = models.CharField('CEP',max_length=12, blank=True)
	email           = models.EmailField('E-mail', max_length=70,blank=True)
	telefone        = models.CharField('Telefone Principal',max_length=20,blank=True)
	atualizado_em   = models.DateTimeField('Atualizado em', auto_now_add=True)
	#complemento
	raca            = models.CharField(max_length=1,choices=RACA)
	estado_civil    = models.CharField(choices=ESTADO_CIVIL,max_length=1)
	profissao       = models.CharField(max_length=50,blank=True)
	convenio        = models.ForeignKey(Convenio,on_delete=models.SET_NULL,null=True,blank=True)
	num_convenio    = models.CharField(max_length=17,blank=True)
	observacao      = models.TextField(max_length=60,blank=True)

	def __str__(self):
		return self.nome

