from django.db import models
from core.utils import STATUS_CONTA,FORMA_PAGAMENTO,PARCELAS,CATEGORIAS,TIPO_CARTAO
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
    valor_pago_dinheiro = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True)
    valor_pago_cartao   = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True)
    convenio            = models.ForeignKey(Convenio,on_delete=models.PROTECT)
    procedimento        = models.ForeignKey(Procedimento,on_delete=models.PROTECT)
    status              = models.CharField(max_length=2,choices=STATUS_CONTA,default='PG')
    forma_pagamento     = models.CharField(max_length=2,choices=FORMA_PAGAMENTO,
    default             ='CV',blank=True,null=True)
    cartao_credito      = models.CharField(max_length=2,choices=TIPO_CARTAO,blank=True,null=True)

    class Meta:
        verbose_name = 'ContaReceber'
        verbose_name_plural = 'ContasReceber'

    def __str__(self):
        return str(self.data) + ' ' + str(self.valor_total)

@receiver(post_save, sender=Atendimento)
def create_conta(sender, instance, created, **kwargs):
    if created:
        if(instance.convenio.nome == 'particular'):
            ContaReceber.objects.create(
            atendimento=instance,
            data=instance.data,
            paciente=instance.paciente,
            profissional=instance.profissional,
            valor_total=instance.procedimento.valor,
            convenio=instance.convenio,
            procedimento=instance.procedimento,
            status='PD',
            forma_pagamento = ''
        )
        else:
            ContaReceber.objects.create(
            atendimento=instance,
            data=instance.data,
            paciente=instance.paciente,
            profissional=instance.profissional,
            valor_total=instance.procedimento.valor,
            convenio=instance.convenio,
            procedimento=instance.procedimento,
            status='PG'
        )
            
def save_conta(sender, instance, **kwargs):
    instance.contareceber.save()
  
class Categoria(models.Model):

    desc = models.CharField(verbose_name='Descrição', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return str(self.desc)

class ContaPagar(models.Model):
    descricao       = models.TextField(verbose_name='Descrição',max_length=200, null=True, blank=True)
    vencimento      = models.DateField(blank=False, null=True)
    valor_total     = models.CharField(null=False, blank=False,max_length=20)
    n_parcela       = models.IntegerField(default=1, choices=PARCELAS,blank=True,verbose_name="Nº Da Parcela")
    status_pag      = models.BooleanField(default=False)
    forma_pagamento = models.CharField(max_length=100, null=False, blank=False, choices=FORMA_PAGAMENTO)
    criado_em       = models.DateTimeField(auto_now_add=True)
    categoria       = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.CASCADE)
    conta_fixa      = models.NullBooleanField(default=False)
    

    class Meta:
        verbose_name = 'Conta a pagar'
        verbose_name_plural = 'Contas a pagar'

    def __str__(self):
        return str(self.descricao)
   
"""
# method for updating
@receiver(post_save, sender=TransactionDetail, dispatch_uid="update_stock_count")
def update_stock(sender, instance, **kwargs):
     instance.product.stock -= instance.amount
     instance.product.save()
"""