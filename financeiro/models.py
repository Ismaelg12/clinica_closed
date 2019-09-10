from django.db import models
from core.utils import STATUS_CONTA,FORMA_PAGAMENTO,PARCELAS,CATEGORIAS,TIPO_CARTAO,RECEPTOR_PAGAMENTO
from atendimento.models import Atendimento
from controle_usuarios.models import Profissional
from pacientes.models import Paciente
from agenda.models import Agendamento
from core.models import Convenio,Procedimento
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from decimal import Decimal

class ContaReceber(models.Model):
    data                = models.DateField()
    agendamento         = models.ForeignKey(Agendamento,on_delete=models.CASCADE)
    paciente            = models.ForeignKey(Paciente,on_delete=models.PROTECT)
    profissional        = models.ForeignKey(Profissional,on_delete=models.PROTECT)
    valor_total         = models.DecimalField(max_digits=6, decimal_places=2)
    valor_inicial       = models.DecimalField(max_digits=6, decimal_places=2,default=Decimal('0.00'))
    valor_pago_dinheiro = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True)
    valor_pago_cartao   = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True)
    convenio            = models.ForeignKey(Convenio,on_delete=models.PROTECT)
    procedimento        = models.ForeignKey(Procedimento,on_delete=models.PROTECT,blank=True,null=True)
    status              = models.CharField(max_length=2,choices=STATUS_CONTA,default='PG')
    forma_pagamento     = models.CharField(max_length=2,choices=FORMA_PAGAMENTO,
    default             ='CV',blank=True)
    cartao_credito      = models.CharField(max_length=2,choices=TIPO_CARTAO,blank=True)
    receptor            = models.CharField(max_length=2,choices=RECEPTOR_PAGAMENTO)
    atualizado_em       = models.DateTimeField('Atualizado em', auto_now=True)
    criado_em           = models.DateTimeField('Criado em', auto_now_add=True)
    

    class Meta:
        verbose_name = 'ContaReceber'
        verbose_name_plural = 'ContasReceber'

    def __str__(self):
        return str(self.data) + ' ' + str(self.valor_total)
"""
@receiver(post_save, sender=Atendimento)
def create_conta(sender, instance, created, **kwargs):
    if created:
        if(instance.convenio.nome == 'particular'):
            ContaReceber.objects.create(
            atendimento=instance,
            data=instance.data,
            paciente=instance.paciente,
            profissional=instance.profissional,
            valor_total=instance.valor,
            convenio=instance.convenio,
            procedimento=instance.procedimento,
            status='PD',
            forma_pagamento = '',
            valor_pago_dinheiro = 00.00 
        )
        else:
            #se for atwndimento com status justificado 
            #ele cai nessa condição por causa que nao tem valor
            if(instance.tipo == 'DM'):
                ContaReceber.objects.create(
                atendimento=instance,
                data=instance.data,
                paciente=instance.paciente,
                profissional=instance.profissional,
                valor_total=00.00,
                convenio=instance.convenio,
                procedimento=instance.procedimento,
                status='PD',
                valor_pago_dinheiro=00.00 
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
                status='PD',
                valor_pago_dinheiro=00.00 
        )

"""
#add
@receiver(post_save, sender=Agendamento)
def create_conta(sender, instance, created, **kwargs):
    if created:
        ContaReceber.objects.create(
        agendamento=instance,
        data=instance.data,
        paciente=instance.paciente,
        profissional=instance.profissional,
        valor_total=instance.valor,
        convenio=instance.convenio,
        valor_inicial=instance.valor,
        status='PD',
        forma_pagamento = '',
        valor_pago_dinheiro = 00.00 
    )

def save_conta(sender, instance, **kwargs):
    instance.contareceber.save()
# method for updating


class Categoria(models.Model):

    desc = models.CharField(verbose_name='Descrição', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return str(self.desc)

class ContaPagar(models.Model):
    profissional    = models.ForeignKey(Profissional,on_delete=models.PROTECT,null=True)
    vencimento      = models.DateField(blank=False, null=True)
    valor_total     = models.CharField(null=False, blank=False,max_length=20)
    n_parcela       = models.IntegerField(default=1, choices=PARCELAS,blank=True,verbose_name="Nº Da Parcela")
    status_pag      = models.BooleanField(default=False)
    forma_pagamento = models.CharField(max_length=100, null=False, blank=False, choices=FORMA_PAGAMENTO)
    categoria       = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.CASCADE)
    conta_fixa      = models.NullBooleanField(default=False)
    atualizado_em   = models.DateTimeField('Atualizado em', auto_now=True)
    criado_em       = models.DateTimeField('Criado em', auto_now_add=True)
    

    class Meta:
        verbose_name = 'Conta a pagar'
        verbose_name_plural = 'Contas a pagar'

    def __str__(self):
        return str(self.vencimento)



@receiver(post_save, sender=ContaReceber)
def contareceber_updated(sender, instance, created, **kwargs):
    if not created:
        # Conta Receber object updated
         ContaPagar.objects.create(
            profissional=instance.profissional,
            vencimento=instance.data,
            valor_total=instance.valor_pago_dinheiro,
            status_pag=False,
            conta_fixa=False,
            forma_pagamento=instance.forma_pagamento,
        )