from django import template

register = template.Library()

@register.filter
def split(value, arg):
    return value.split(arg)

@register.filter
def strip(value):
    return value.strip()

@register.filter
def splitlines(value):
    if value:
        return value.splitlines()
    return [] 