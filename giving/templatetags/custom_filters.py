from django import template
from math import ceil

register = template.Library()

@register.filter(name="roundup")
def roundup(value):
    return ceil(value)