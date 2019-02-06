from django.db import models
from core.utils import STATUS_CONTA,FORMA_PAGAMENTO
from atendimento.models import Atendimento
from controle_usuarios.models import Profissional
from pacientes.models import Paciente
from core.models import Convenio,Procedimento
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver

class ContaReceber(models.Model):
	data                = models.DateTimeField()
	atendimento         = models.ForeignKey(Atendimento,on_delete=models.CASCADE)
	paciente            = models.ForeignKey(Paciente,on_delete=models.PROTECT)
	profissional        = models.ForeignKey(Profissional,on_delete=models.PROTECT)
	valor_total         = models.DecimalField(max_digits=6, decimal_places=2)
	valor_pago_dinehiro = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True)
	valor_pago_cartao   = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True)
	convenio            = models.ForeignKey(Convenio,on_delete=models.PROTECT)
	procedimento        = models.ForeignKey(Procedimento,on_delete=models.PROTECT)
	status              = models.CharField(max_length=2,choices=STATUS_CONTA,default='PD')
	forma_pagamento     = models.CharField(max_length=2,choices=FORMA_PAGAMENTO,
	default             ='CV')

	class Meta:
		verbose_name = 'ContaReceber'
		verbose_name_plural = 'ContasReceber'

	def __str__(self):
		return str(self.data) + ' ' + str(self.valor_total)

@receiver(post_save, sender=Atendimento)
def create_conta(sender, instance, created, **kwargs):
    if created:
        ContaReceber.objects.create(
        	atendimento=instance,
        	data=instance.data,
        	paciente=instance.paciente,
        	profissional=instance.profissional,
        	valor_total=instance.procedimento.valor,
        	convenio=instance.convenio,
        	procedimento=instance.procedimento,
        )

def save_conta(sender, instance, **kwargs):
    instance.contareceber.save()
    
"""
# method for updating
@receiver(post_save, sender=TransactionDetail, dispatch_uid="update_stock_count")
def update_stock(sender, instance, **kwargs):
     instance.product.stock -= instance.amount
     instance.product.save()
"""