# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from controle_usuarios.utils import AREA


# First, define the Manager subclass.
class ProfissinalManager(models.Manager):
	def get_queryset(self):
		return super().get_queryset().filter(ativo=True).exclude(user__username="admin")

#Modelo para a area de atuação de cada Profissional
class Perfil(models.Model):
	id = models.PositiveSmallIntegerField(choices=AREA,primary_key=True)

	def __str__(self): 
		return self.get_id_display()

class Profissional(models.Model):
	ATENDENTE = 1
	MEDICO = 2
	ROLE_CHOICES = (
		(1, 'Atendente'),
		(2, 'Profissional'),
	)
	nome            = models.CharField(max_length=50)
	sobrenome       = models.CharField(max_length=50)
	user            = models.OneToOneField(User, on_delete=models.CASCADE)
	email           = models.EmailField(max_length=50,blank=True,null=True)
	telefone        = models.CharField(max_length=15,blank=True)
	registro        = models.CharField(max_length=16,blank=True)
	cpf             = models.CharField(max_length=14,unique=True,null=True)
	data_nascimento = models.DateField(null=True,blank=True)
	tipo            = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,verbose_name='Tipo (Permissão)',null=True)
	area_atuacao    = models.ManyToManyField(Perfil)
	quantidade_atend= models.IntegerField(blank=True,choices=list(zip(range(1, 11), range(1, 11))),null=True)
	data_cadastro   = models.DateField(auto_now_add = True)
	horario_trabalho= models.CharField('Dias de Trabalho',max_length=12,blank=True)
	ativo           = models.BooleanField(default=True)
	atualizado_em   = models.DateTimeField('Atualizado em', auto_now=True)
	atent_categoria	= models.CharField('Tipos de atendimentos',max_length=200,blank=True)
	abordagem		= models.CharField('Abordagens',max_length=200,blank=True)
	observacao		= models.CharField('Outras Observações',max_length=200,blank=True)
	conta_banco		= models.TextField('Contas bancarias', blank=True)
	
	objects = models.Manager() # The default manager.
	#manage Sobrescrito
	prof_objects = ProfissinalManager() 

	class Meta:
		verbose_name = 'Profissional'
		verbose_name_plural = 'Profissionais'

	def __str__(self):
		return self.nome + ' ' + self.sobrenome

#signals para atualizar o email nos dois modelos
@receiver(post_save, sender=Profissional)
def update_profissional_user(sender, instance, created, **kwargs):
	if not created:
		if instance.email != None:
			User.objects.filter(id=instance.id).update(email=instance.email)
		
#signals para criar o profissional junto ao user
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profissional.objects.create(
			user=instance)
	instance.profissional.save()

@receiver(post_delete, sender=Profissional)
def auto_delete(sender, instance, **kwargs):
	instance.user.delete()