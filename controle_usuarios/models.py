# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from core.utils import AREA
class Profissional(models.Model):
	ATENDENTE = 1
	MEDICO = 2
	ROLE_CHOICES = (
		(1, 'Atendente'),
		(2, 'Profissional'),
	)
	nome            = models.CharField(max_length=50)
	sobrenome       = models.CharField(max_length=50)
	user            = models.OneToOneField(User, on_delete=models.CASCADE,)
	email           = models.EmailField(max_length=50, blank=True)
	telefone        = models.CharField(max_length=15, blank=True)
	registro        = models.CharField(max_length=12, blank=True)
	cpf             = models.CharField(max_length=14,unique=True,null=True)
	data_nascimento = models.DateField(null=True, blank=True)
	tipo            = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
	area_atuacao    = models.CharField(max_length=2,blank=True,null=True,choices=AREA)
	quantidade_atend= models.IntegerField(blank=True,choices=list(zip(range(1, 11), range(1, 11))),null=True)
	data_cadastro   = models.DateField(auto_now_add = True)
	ativo           = models.BooleanField(default=True)
	class Meta:
		verbose_name = 'Profissional'
		verbose_name_plural = 'Profissionais'

	def __str__(self):
		return self.nome + ' ' + self.sobrenome
		
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profissional.objects.create(user=instance)
    instance.profissional.save()

@receiver(post_delete, sender=Profissional)
def auto_delete(sender, instance, **kwargs):
    instance.user.delete()