from django import template

register = template.Library()


@register.filter
def to_dot(value):
    return str(value).replace(',', '.')
