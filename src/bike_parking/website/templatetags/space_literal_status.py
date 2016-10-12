from django import template
from parking.models import parking_space_status

register = template.Library()


@register.filter
def space_literal_status(value):
    return dict(parking_space_status)[value]
