import re

from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag(takes_context=True)
def historytype(context, type):
    if type == '+':
        return 'history_create'
    
    if type == '~':
        return 'history_change'

    if type == '-':
        return 'history_delete'