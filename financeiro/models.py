from django.db import models
from core.utils import STATUS_CONTA,FORMA_PAGAMENTO,PARCELAS,CATEGORIAS,TIPO_CARTAO,RECEPTOR_PAGAMENTO
from atendimento.models import Atendimento
from django.contrib.auth.models import User
from controle_usuarios.models import Profissional
from pacientes.models import Paciente
from agenda.models import Agendamento
from core.models import Convenio,Procedimento
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from decimal import Decimal

DESCONTO_CHOICES =( 
    ('', 'Escolha um desconto'),
    ('0.95','5 %'),
    ('0.90', '10 %'),
    ('0.85', '15 %'),
    ('0.80', '20 %'),
    ('0.75', '25 %'),
    ('0.70', '30 %'),
    ('0.65', '35 %'),
    ('0.60', '40 %'),
    ('0.55', '45 %'),
    ('0.50', '50 %'),
)

class ContaReceber(models.Model):
    data                = models.DateField()
    agendamento         = models.ForeignKey(Agendamento,on_delete=models.CASCADE,blank=True, null=True)
    paciente            = models.ForeignKey(Paciente,on_delete=models.PROTECT)
    profissional        = models.ForeignKey(Profissional,on_delete=models.PROTECT)
    valor_total         = models.DecimalField(max_digits=6, decimal_places=2)
    desconto            = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True,default=Decimal('0.00'))
    valor_total_pago    = models.DecimalField(max_digits=6, decimal_places=2,default=Decimal('0.00'),blank=True,)
    valor_pago_dinheiro = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True)
    valor_pago_cartao   = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True,default=Decimal('0.00'))
    status              = models.CharField(max_length=2,choices=STATUS_CONTA,default='PG')
    forma_pagamento     = models.CharField(max_length=2,choices=FORMA_PAGAMENTO,
    default             ='ES',blank=True)
    recebido_por        = models.CharField('recebido_por',max_length=50,blank=True)
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
        if(instance.convenio.nome == 'particular'): 
            ContaReceber.objects.create(
                agendamento=instance,
                data=instance.data,
                paciente=instance.paciente,
                profissional=instance.profissional,
                valor_total=instance.valor,
                status='PD',
                forma_pagamento = '',
                valor_pago_dinheiro = 00.00 
            )
    else:
        pass
        #insere na tabela de convenio

def save_conta(sender, instance, **kwargs):
    instance.contareceber.save()

# method for updating agendamento
@receiver(post_save, sender=Agendamento, dispatch_uid="estorno_conta_receber")
def estorno_conta_receber(sender, instance, **kwargs):
    #cancela o registro financeiro  relacioando
   if(instance.status == 'FJ' or instance.status == 'DM'):
        print("conta")
        contas = ContaReceber.objects.filter(agendamento=instance.id)
        for c in contas:
            c.delete()
            print('deletado')


class Categoria(models.Model):

    desc = models.CharField(verbose_name='Descrição', max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return str(self.desc)

class ContaPagar(models.Model):
    profissional    = models.ForeignKey(Profissional,on_delete=models.PROTECT,null=True)
    paciente        = models.ForeignKey(Paciente,on_delete=models.PROTECT)
    data            = models.DateField(blank=False, null=True)
    valor_total     = models.CharField(null=False, blank=False,max_length=20)
    status_pag      = models.BooleanField(default=False)
    hora_inicio     = models.TimeField()
    hora_final      = models.TimeField()
    atualizado_em   = models.DateTimeField('Atualizado em', auto_now=True)
    criado_em       = models.DateTimeField('Criado em', auto_now_add=True)
    

    class Meta:
        verbose_name = 'Conta a pagar'
        verbose_name_plural = 'Contas a pagar'

    def __str__(self):
        return str(self.data)



@receiver(post_save, sender=ContaReceber)
def contareceber_updated(sender, instance, created, **kwargs):
    if not created:
        # Conta Receber object updated
         ContaPagar.objects.create(
            profissional=instance.profissional,
            data=instance.data,
            valor_total=instance.valor_total_pago,
            paciente=instance.paciente,
            #nao funciona ainda
            hora_inicio='14:00',
            hora_final='14:00',
        )

class Lote(models.Model):
    criado_em           = models.DateTimeField('Criado em', auto_now_add=True)
    def __str__(self):
        return str(self.criado_em)

#financeiro dos convenios
class Faturamento(models.Model):
    data_guia           = models.DateField()
    numero_guia         = models.CharField('Numero da guia',max_length=20,blank=True)
    lote                = models.ForeignKey(Lote,on_delete=models.CASCADE,null=True)
    #mudar pra atendimento  
    atendimento         = models.ForeignKey(Atendimento,on_delete=models.CASCADE,blank=True, null=True)
    paciente            = models.ForeignKey(Paciente,on_delete=models.PROTECT)
    profissional        = models.ForeignKey(Profissional,on_delete=models.PROTECT)
    valor_unitario      = models.DecimalField(max_digits=6, decimal_places=2,blank=True,null=True,default=Decimal('0.00'))
    servico             = models.CharField('Serviço',max_length=50,blank=True)
    procedimento        = models.CharField('Procedimento',max_length=50,blank=True)
    cod_procedimento    = models.CharField('codigo',max_length=50,blank=True)
    status_pag          = models.BooleanField(default=False)
    status_fat          = models.BooleanField(default=False)
    status_nf           = models.BooleanField(default=False)
    criado_em           = models.DateTimeField('Criado em', auto_now_add=True)
    

    class Meta:
        verbose_name = 'Faturamento'
        verbose_name_plural = 'Faturamentos'

    def __str__(self):
        return str(self.data_guia) + ' ' + str(self.paciente)

#add
@receiver(post_save, sender=Atendimento)
def create_faturamento(sender, instance, created, **kwargs):
    if created:
        if(instance.convenio.nome != 'particular'): 
            Faturamento.objects.create(
                atendimento=instance,
                data_guia=instance.guia.validade,
                numero_guia=instance.guia.numero,
                paciente=instance.paciente,
                profissional=instance.profissional,
                valor_unitario=instance.guia.procedimento.valor,
                procedimento=instance.procedimento,
                cod_procedimento=instance.procedimento.codigo,
                servico = instance.profissional.area_atuacao
            )

def save_conta_faturamento(sender, instance, **kwargs):
    instance.faturamento.save()


class ReciboPago(models.Model):
    profissional = models.ForeignKey(Profissional,on_delete=models.CASCADE)
    data_upload  = models.DateTimeField(auto_now_add=True)
    documento    = models.FileField(upload_to='recibos/%Y/%m/%d/')

    def __str__(self):
        return str(self.profissional)
