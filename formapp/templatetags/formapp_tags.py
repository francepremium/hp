from django import template
from django.utils.safestring import mark_safe

from formapp.models import Record

register = template.Library()


@register.filter
def render_value(value):
    if isinstance(value, list):
        value = Record.objects.filter(pk__in=value)
        value = mark_safe(u', '.join(
            ['<a href="%s">%s</a>' % (
                r.get_absolute_url(), unicode(r)) for r in value]))
    return value


@register.filter
def get_field(form, name):
    return form[name]
