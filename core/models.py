from django.db import models
from core.utils import SEXO,AREA
from controle_usuarios.models import Profissional
class Convenio(models.Model):
	nome          = models.CharField(max_length=40)
	atualizado_em = models.DateTimeField('Atualizado em', auto_now_add=True)
	ativo         = models.BooleanField(default=True)
	class Meta:
		verbose_name = 'Convenio'
		verbose_name_plural = 'Convenios'

	def __str__(self):
		return self.nome


class Sala(models.Model):
	nome          = models.CharField(max_length=40)
	descricao     = models.TextField(blank=True)
	atualizado_em = models.DateTimeField('Atualizado em', auto_now_add=True)

	class Meta:
		verbose_name = 'Sala'
		verbose_name_plural = 'Salas'

	def __str__(self):
		return self.nome

class Procedimento(models.Model):
	codigo        = models.IntegerField()
	nome          = models.CharField(max_length=50)
	convenio      = models.ForeignKey(Convenio,on_delete=models.SET_NULL,null=True,blank=True)
	valor         = models.DecimalField(max_digits=6, decimal_places=2)
	descricao     = models.TextField(blank=True)
	atualizado_em = models.DateTimeField('Atualizado em', auto_now_add=True)
	ativo         = models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Procedimento'
		verbose_name_plural = 'Procedimentos'

	def __str__(self):
		return str(self.codigo) + ' : '+ self.nome

class ListaEspera(models.Model):
	#informações basicas
	nome            = models.CharField(max_length=40)
	data_nascimento = models.DateField()
	sexo            = models.CharField('Sexo', max_length=1, choices=SEXO, blank=True)
	area_atuacao    = models.CharField(max_length=2,blank=True,null=True,choices=AREA)
	profissional    = models.ForeignKey(Profissional,on_delete=models.PROTECT)
	telefone        = models.CharField('Telefone Principal',max_length=20,blank=True)
	atualizado_em   = models.DateTimeField('Atualizado em', auto_now_add=True)
	observacao      = models.TextField(max_length=60,blank=True)

	class Meta:
		verbose_name = 'Lista de Espera'
		verbose_name_plural = 'Listas de Espera'

	def __str__(self):
		return self.nome
