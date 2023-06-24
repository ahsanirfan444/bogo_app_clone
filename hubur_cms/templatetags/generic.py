from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime
from django.utils.timesince import timesince

register = template.Library()

@register.filter(name="format_date")
@stringfilter
def format_date(value):
    return str(datetime.strptime(value, "%Y-%m-%d").date())

@register.filter(name="format_time")
@stringfilter
def format_time(value):
    try:
        return str(datetime.strptime(value, "%H:%M:%S").time())
    except ValueError:
        return ""

@register.filter(name='discountPercentage')
def discountPercentage(value1, value2):
    try:
        return round(value1 - ((value1 / 100) * value2), 2)

    except Exception:
        return 0
    
@register.filter(name='timeDuration')
def timeDuration(value):
    return timesince(value).split(", ")[0]


@register.filter(name='abs')
def abs(value):
    return abs(value)


@register.simple_tag()
def multiply(value1, value2):
    return value1 * value2


@register.filter(name='percentage')
def percentage(value1, value2):
    return round(((value1 / 100 ) * value2), 2)


@register.filter(name='divide')
def divide(value1, value2):
    try:
        value = round((value2 /  value1), 2)
        return value
    except Exception:
        return 0