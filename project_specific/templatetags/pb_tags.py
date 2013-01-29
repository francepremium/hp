from django import template

from formapp.models import Record

register = template.Library()


@register.filter
def render_title(record):
    if 'titre' not in record.data or not record.data.get('auteur', False):
        return unicode(record)

    author = Record.objects.get(pk=record.data['auteur'][0])

    return u'%s / %s %s' % (record.data['titre'], author.data['prenom'],
            author.data['nom'])
