# -*- coding: utf-8 -*-
from django.db.models import Count
import datetime
from pacientes.models import Paciente
from core.models import Convenio
from atendimento.models import Agendamento
from django.utils import timezone
class DashboardMixin(object):
	def clientes(self):
		return Paciente.objects.all().count()
	#def convenios(self):
		#return Convenio.objects.all().count()
	def birthday(self):
		today     = timezone.now().date()
		return Paciente.objects.filter(data_nascimento__day=today.day,data_nascimento__month=today.month).count()
	def agendamentos(self):
		today = timezone.now().date()
		return Agendamento.objects.filter(data__day=today.day,data__month=today.month).count()