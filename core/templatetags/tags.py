from django import template
from atendimento.models import Agendamento
register = template.Library()

@register.filter
def subtract(value, arg):
    if arg > value:
        return 0
    else:
        return value - arg
