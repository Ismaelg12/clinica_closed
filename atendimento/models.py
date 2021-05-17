# -*- coding: utf-8 -*-
from django.db import models
import datetime
from django.utils import timezone
from core.models import Sala,Convenio,Procedimento
from pacientes.models import Paciente
from controle_usuarios.models import Profissional
from core.utils import TIPO_ATENDIMENTO,STATUS,TIPO_GUIA,STATUS_GUIA
from django.core.validators import MaxValueValidator, MinValueValidator

'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           Models de Atendimento
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

#Cabecalho de todos os atendimentos
class Atendimento(models.Model):
    tipo          = models.CharField(max_length=2,blank=True,
        choices=TIPO_ATENDIMENTO)
    data          = models.DateField()
    paciente      = models.ForeignKey(Paciente,on_delete=models.PROTECT)
    hora_inicio   = models.TimeField()
    hora_fim      = models.TimeField()
    convenio      = models.ForeignKey(Convenio,on_delete=models.PROTECT)
    procedimento  = models.ForeignKey(Procedimento,on_delete=models.PROTECT,blank=True,null=True)
    profissional  = models.ForeignKey(Profissional,on_delete=models.PROTECT)
    guia          = models.ForeignKey('Guia',on_delete=models.PROTECT,blank=True,null=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    criado_em     = models.DateTimeField('Criado em', auto_now_add=True)


    class Meta:
        verbose_name = 'Atendimento'
        verbose_name_plural = 'Atendimentos'

    def __str__(self):
        return str(self.paciente) + ' '+ str(self.convenio)+ ' ' +str(self.procedimento)

        
#atendimento evolução
class Evolucao(models.Model):
    atendimento   = models.OneToOneField(Atendimento,on_delete=models.CASCADE,primary_key=True)
    evolucao      = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Evolução'
        verbose_name_plural = 'Evoluções'

    def __str__(self):
        return "{}".format(self.atendimento)

#atendimento avaliação
class Avaliacao(models.Model):
    atendimento          = models.OneToOneField(Atendimento,on_delete=models.CASCADE,primary_key=True)
    queixa               = models.TextField('Queixa Principal',max_length=400,blank=True)
    familia              = models.TextField('Histórico Familiar',max_length=400,blank=True)
    patologico           = models.TextField('Histórico Patológico',max_length=400,blank=True)
    social               = models.TextField('HIstórico Social',max_length=400,blank=True)
    condulta             = models.TextField('Condulta',max_length=400,blank=True)

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'

    def __str__(self):
        return "{}".format(self.atendimento)
        
class Guia(models.Model):
    numero           = models.CharField(max_length=20)
    convenio         = models.ForeignKey(Convenio,on_delete=models.SET_NULL,null=True,blank=True)
    paciente         = models.ForeignKey(Paciente,on_delete=models.PROTECT)
    #profissional     = models.ForeignKey(Profissional,on_delete=models.PROTECT)
    profissional     = models.ManyToManyField(Profissional)
    procedimento     = models.ForeignKey(Procedimento,on_delete=models.CASCADE)
    quantidade       = models.IntegerField()
    qtdautorizada    = models.IntegerField()
    validade         = models.DateField()
    data_autorizacao = models.DateField()
    tipo_guia        = models.CharField(max_length=2,choices=TIPO_GUIA,default='PM')
    status           = models.CharField(max_length=1,choices=STATUS_GUIA,default='N')
    validada         = models.BooleanField(default=False)
    atualizado_em    = models.DateTimeField('Atualizado em', auto_now=True)
    criado_em        = models.DateTimeField('Criado em', auto_now_add=True)
    ativo            = models.BooleanField(default=True)

    class Meta:
        verbose_name        = 'Guia'
        verbose_name_plural = 'Guias'
        ordering            = ['quantidade']

    def __str__(self):
        return str(self.numero) + ' | ' + str(
            self.procedimento)+ ' | ' + str(self.quantidade)+ ' | ' + str(self.validade)
    
    #propriedade para notificar guias vencidas com alertas
    @property
    def verifica_vencimento(self):
        data_atual      = datetime.date.today()
        futuro          = self.validade - datetime.timedelta(days=7)

        if data_atual > self.validade:
            return "Vencido"
        elif data_atual > futuro and data_atual < self.validade:
            return "Alerta"
        else:
            return "Valido"

   