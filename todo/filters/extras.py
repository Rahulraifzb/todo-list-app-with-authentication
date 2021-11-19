from django import template

register = template.Library()

@register.simple_tag
def define(val=None):
    if val:
        return "text-decoration-strike"
    return "text-decoration-none"