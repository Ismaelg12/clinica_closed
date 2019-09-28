# -*- coding: utf-8 -*-
from django.db.models import Count
import datetime
from pacientes.models import Paciente
from atendimento.models import Guia
from core.models import Convenio
from agenda.models import Agendamento
from django.utils import timezone
from controle_usuarios.models import Profissional

class DashboardMixin(object):
	
	def clientes(self):
		profissional = Profissional.objects.filter(
			user=self.request.user,tipo=2)

		if profissional:
			paciente_count = Paciente.objects.filter(
				profissional=profissional[0]).count()
		else:
			paciente_count = Paciente.objects.all().count()
		return paciente_count
	#def convenios(self):
		#return Convenio.objects.all().count()

	def birthday(self):
		today     = timezone.now().date()
		return Paciente.objects.filter(data_nascimento__day=today.day,
			data_nascimento__month=today.month).count()
	
	def agendamentos(self):
		profissional = Profissional.objects.filter(
			user=self.request.user,tipo=2)
		today = timezone.now().date()
		if profissional:
			agenda_count = Agendamento.objects.filter(data__day=today.day,
			data__month=today.month,profissional=profissional[0],status='AG').count()
		else:
			agenda_count = Agendamento.objects.filter(data__day=today.day,
			data__month=today.month,status='AG').count()
		return agenda_count

	def guias_count(self):
		profissional = Profissional.objects.filter(
			user=self.request.user,tipo=2)

		if profissional:
			guia_count = Guia.objects.filter(
				profissional=profissional[0],ativo=True).count()
		else:
			guia_count = Guia.objects.filter(ativo=True).count()
		return guia_count