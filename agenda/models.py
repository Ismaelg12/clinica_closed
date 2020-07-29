# -*- coding: utf-8 -*-
from django.db import models
import datetime
from django.utils import timezone
from core.models import Sala,Convenio,Procedimento
from pacientes.models import Paciente
from controle_usuarios.models import Profissional
from atendimento.models import Guia,Atendimento
from core.utils import STATUS
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
'''
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
+                           Models de Agendamento
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
'''

class Agendamento(models.Model):
    id            = models.AutoField(primary_key=True)
    data          = models.DateField(null=True)
    hora_inicio   = models.TimeField(null=True)
    hora_fim      = models.TimeField(null=True)
    paciente      = models.ForeignKey(Paciente,on_delete=models.PROTECT)
    profissional  = models.ForeignKey(Profissional,on_delete=models.PROTECT, blank=True)
    telefone      = models.CharField(max_length=15,blank=True)
    observacao    = models.TextField(blank=True)
    sala          = models.ForeignKey(Sala,on_delete=models.SET_NULL,null=True,blank=True)
    criado_em     = models.DateTimeField('Criado em', auto_now_add=True)
    status        = models.CharField(max_length=2,choices=STATUS,default='AG',blank=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    convenio      = models.ForeignKey(Convenio,on_delete=models.PROTECT)
    cancelado     = models.TextField(blank=True,max_length=50)
    liberado      = models.BooleanField(default=False)
    valor         = models.DecimalField('Valor do Atendimento',
        max_digits=6, decimal_places=2,null=True,blank=True, default=Decimal(0.00))
    #pago          = models.BooleanField('pagamento', default=False)
    pacote        = models.BooleanField('pacote', default=False)
    
    

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
    
    def __str__(self):
        return self.paciente.nome
    

# method for updating guia
@receiver(post_save, sender=Agendamento, dispatch_uid="update_decrement_guia_count")
def update_decrement_guia(sender, instance, **kwargs):
    #cancela todos os agendamentos relacioandos
    if(instance.status == 'CC'): 
        agendamentos = Agendamento.objects.filter(
            paciente_id=instance.paciente.id,status="AG",
            profissional_id=instance.profissional.id
        )
        for ag in agendamentos:
            ag.status = "CC"
            ag.save()
 
   
