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

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return self.paciente.nome + ' '+ str(self.data)
    """
    class MyModel(models.Model):
    f1 = models.CharField(max_length=1)
    
    def save(self, *args, **kw):
        if self.pk is not None:
            orig = MyModel.objects.get(pk=self.pk)
            if orig.f1 != self.f1:
                print 'f1 changed'
        super(MyModel, self).save(*args, **kw)
    """
    """
    # override do metodo save para saber se existe um agendamento igual antes de salvar
    def save(self, *args, **kwargs):
       # start_date = datetime.datetime.strptime('09-01-2019','%d-%m-%Y')
        #print('datetime',datetime.date.today())
        #print("self",self.data)
        agendamento = Agendamento.objects.filter(data=self.data,status='AG')
        #print("agendamnetos de hoje!!",agendamento)
        for i in agendamento:
            print(i.data,i.paciente,i.sala,i.profissional)
            if((i.data == self.data ) and (i.hora_inicio == self.hora_inicio) and (
                i.hora_fim == self.hora_fim) and(i.sala == self.sala)):
                print("Esse Agendamento não pode ser salvo pq ja existe um igual no banco:(")
                break
            super(Agendamento, self).save(*args, **kwargs)
    """
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
        return self.tipo
    

