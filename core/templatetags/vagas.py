from django import template
register = template.Library()

@register.filter
def subtract(value, arg):
    if arg > value:
        return 0
    else:
        return value - arg