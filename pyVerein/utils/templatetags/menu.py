import re

from django import template
from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()


@register.simple_tag(takes_context=True)
def url_class(context, pattern_or_urlname, class_name):
    try:
        pattern = '^' + reverse(pattern_or_urlname) + "$"
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return class_name
    return ''

@register.simple_tag(takes_context=True)
def base_url_class(context, pattern_or_urlname, class_name):
    try:
        pattern = '^' + reverse(pattern_or_urlname)
    except NoReverseMatch:
        pattern = pattern_or_urlname
    path = context['request'].path
    if re.search(pattern, path):
        return class_name
    return ''