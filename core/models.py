from django.db import models
from core.utils import SEXO,CONVENIOS,UF
from controle_usuarios.utils import AREA
from controle_usuarios.models import Profissional
from django.core.validators import MaxValueValidator, MinValueValidator

class Convenio(models.Model):
	nome          = models.CharField(max_length=40,choices=CONVENIOS)
	atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
	criado_em     = models.DateTimeField('Criado em', auto_now_add=True)
	ativo         = models.BooleanField(default=True)
	
	class Meta:
		verbose_name = 'Convenio'
		verbose_name_plural = 'Convenios'

	def __str__(self):
		return self.nome.upper()


class Sala(models.Model):
	nome          = models.CharField(max_length=40)
	descricao     = models.TextField(blank=True)
	atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
	criado_em     = models.DateTimeField('Criado em', auto_now_add=True)

	class Meta:
		verbose_name = 'Sala'
		verbose_name_plural = 'Salas'

	def __str__(self):
		return self.nome


class Procedimento(models.Model):
	codigo        = models.CharField(max_length=20)
	nome          = models.CharField(max_length=50)
	convenio      = models.ForeignKey(Convenio,on_delete=models.SET_NULL,null=True,blank=True)
	valor         = models.DecimalField(max_digits=6, decimal_places=2)
	descricao     = models.TextField(blank=True)
	atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
	criado_em     = models.DateTimeField('Criado em', auto_now_add=True)
	ativo         = models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Procedimento'
		verbose_name_plural = 'Procedimentos'

	def __str__(self):
		return str(self.codigo) + ' - ' + str(self.nome)


class ListaEspera(models.Model):
	#informações basicas
	nome            = models.CharField(max_length=40)
	idade           = models.IntegerField(validators=[MaxValueValidator(100),MinValueValidator(1)])
	data_nascimento = models.DateField()
	sexo            = models.CharField('Sexo', max_length=1, choices=SEXO, blank=True)
	turno_manha     = models.BooleanField(blank=True,default=False)
	turno_tarde     = models.BooleanField(blank=True,default=False)
	turno_noite     = models.BooleanField(blank=True,default=False)
	especialidade   = models.IntegerField(blank=True,null=True,choices=AREA)
	profissional    = models.ManyToManyField(Profissional)
	#profissional   = models.ForeignKey(Profissional,on_delete=models.PROTECT)
	telefone        = models.CharField('Telefone Principal',max_length=20,blank=True)
	atualizado_em   = models.DateTimeField('Atualizado em', auto_now=True)
	criado_em       = models.DateTimeField('Criado em', auto_now_add=True)
	observacao      = models.TextField(max_length=200,blank=True)

	class Meta:
		verbose_name = 'Lista de Espera'
		verbose_name_plural = 'Listas de Espera'

	def __str__(self):
		return self.nome


class Clinica(models.Model):
	logo_menu  	= models.ImageField(upload_to='media')
	clinica    	= models.CharField(max_length=50,blank=True)
	sobre_nos	= models.TextField(max_length=600,blank=True)	
	keywords	= models.CharField(max_length=400,blank=True)
	cidade      = models.CharField(max_length=20,blank=True)
	rua      = models.CharField(max_length=40,blank=True)
	bairro      = models.CharField(max_length=20,blank=True)
	telefone      = models.CharField(max_length=20,blank=True)
	email      = models.CharField(max_length=40,blank=True)

	class Meta:
		verbose_name = 'Clinica '
		verbose_name_plural = 'Clinica'
		
	def __str__(self):
		return self.clinica

