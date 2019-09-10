from django.contrib import admin
#from pacientes.models import Paciente
from django.forms import CheckboxSelectMultiple
from pacientes.models import *

class PacienteAdmin(admin.ModelAdmin):
	list_display = ['nome','telefone','convenio','telefone','data_nascimento']
	search_fields  = ['nome']
	formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
admin.site.register(Paciente,PacienteAdmin)