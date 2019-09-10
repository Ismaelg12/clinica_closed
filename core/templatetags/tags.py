from django import template
from agenda.models import Agendamento
register = template.Library()

@register.filter
def subtract(value, arg):
    #realiza subtrações de modelos
    if float(arg) > value:
        return 0
    else:
        return value - arg
