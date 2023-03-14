from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime

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
