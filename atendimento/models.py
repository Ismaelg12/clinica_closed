# -*- coding: utf-8 -*-
from django.db import models
import datetime
from django.utils import timezone
from core.models import Sala,Convenio,Procedimento
from pacientes.models import Paciente
from controle_usuarios.models import Profissional
from core.utils import ATENDIMENTO,STATUS

'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           Models de Agendamento
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

class Agendamento(models.Model):
    data         = models.DateField()
    hora_inicio  = models.TimeField()
    hora_fim     = models.TimeField()
    sala         = models.ForeignKey(Sala, on_delete=models.SET_NULL,null=True)
    paciente     = models.ForeignKey(Paciente,on_delete=models.PROTECT)
    convenio     = models.ForeignKey(Convenio,on_delete=models.PROTECT)
    profissional = models.ForeignKey(Profissional,on_delete=models.PROTECT)
    telefone     = models.CharField(max_length=15,blank=True)
    status       = models.CharField(max_length=2,choices=STATUS,default='AG',blank=True)
    observacao   = models.TextField(blank=True)
    cancelado    = models.TextField(blank=True,max_length=50)
    liberado     = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return self.paciente.nome + ' '+ str(self.data)
        
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           Models de Atendimento
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

class Atendimento(models.Model):
    tipo         = models.CharField(max_length=2,choices=ATENDIMENTO)
    data         = models.DateField()
    paciente     = models.ForeignKey(Paciente,on_delete=models.PROTECT)
    hora_inicio  = models.TimeField()
    hora_fim     = models.TimeField()
    convenio     = models.ForeignKey(Convenio,on_delete=models.PROTECT)
    procedimento = models.ForeignKey(Procedimento,on_delete=models.PROTECT)
    profissional = models.ForeignKey(Profissional,on_delete=models.PROTECT)
    guia         = models.ForeignKey('Guia',on_delete=models.PROTECT)
    ##############avaliação######################
    qp                 = models.TextField(blank=True)
    diagnostico        = models.TextField(blank=True)
    hda                = models.TextField(blank=True)
    outras_doencas     = models.TextField(blank=True)
    pa                 = models.CharField(max_length=15,blank=True)
    mmHg               = models.CharField(max_length=15,blank=True)
    bpm                = models.CharField(max_length=15,blank=True)
    rpm                = models.CharField(max_length=15,blank=True)
    inspecao           = models.TextField(blank=True)
    palpacao           = models.TextField(blank=True)
    exame_fisico1      = models.TextField(blank=True)
    exame_fisico2      = models.TextField(blank=True)
    exame_complementar = models.TextField(blank=True)
    teste_especifico   = models.TextField(blank=True)
    tratamento         = models.TextField(blank=True)
    ####################Evolução###################
    evolucao           = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Atendimento'
        verbose_name_plural = 'Atendimentos'

    def __str__(self):
        return self.tipo + ' ' +str(self.data) 

class Guia(models.Model):
    numero        = models.IntegerField()
    convenio      = models.ForeignKey(Convenio,on_delete=models.SET_NULL,null=True,blank=True)
    paciente      = models.ForeignKey(Paciente,on_delete=models.PROTECT)
    profissional  = models.ForeignKey(Profissional,on_delete=models.PROTECT)
    descricao     = models.TextField(blank=True)
    quantidade    = models.IntegerField()
    validade      = models.DateField()
    data_cadastro = models.DateField(auto_now_add = True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now_add=True)
    ativo         = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Guia'
        verbose_name_plural = 'Guias'

    def __str__(self):
        return str(self.numero) + ' : ' +str(self.quantidade)