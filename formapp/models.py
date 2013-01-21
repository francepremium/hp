import sys

from django.core.urlresolvers import reverse
from django.db import models
from django.forms.models import ModelMultipleChoiceField
from django.db.models import signals
from django.utils.translation import ugettext as _
from django.db.models.signals import pre_save

import jsonfield
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField

from form_designer.models import Widget, Form


def unicode_truncate(s, length, encoding='utf-8'):
    encoded = s.encode(encoding)[:length]
    return encoded.decode(encoding, 'ignore')


class Record(models.Model):
    form = models.ForeignKey('form_designer.Form')
    environment = models.ForeignKey('appstore.Environment')

    data = jsonfield.JSONField(db_type='json')
    text_data = models.TextField()

    search_index = VectorField()
    objects = SearchManager(
        fields=('text_data',),
        auto_update_search_field=True
    )

    def get_absolute_url(self):
        return reverse('formapp_record_detail', args=(self.pk,))

    def __unicode__(self):
        bits = []

        i = 0
        for key, value in self.data.items():
            if not value:
                continue

            if isinstance(value, basestring):
                bits.append(value)

        if not bits:
            return u'%s #%s' % (self.form.verbose_name, self.pk)

        return u', '.join(bits)

    @property
    def feature(self):
        return self.form.appform.app.provides


def text_data(sender, instance, **kwargs):
    data = []

    for value in instance.data.values():
        if not value:
            continue
        elif isinstance(value, list):
            # We are avoiding recursion on purpose
            for pk in value:
                related = Record.objects.get(pk=pk)
                for related_value in related.data.values():
                    if not related_value:
                        continue
                    data.append(unicode(related_value))
        else:
            data.append(unicode(value))

    instance.text_data = unicode_truncate(u' '.join(data), 1000)
    print len(instance.text_data), sys.getsizeof(instance.text_data)
pre_save.connect(text_data, sender=Record)


class RecordMultipleChoiceField(ModelMultipleChoiceField):
    def __init__(self, queryset, **kwargs):
        if isinstance(queryset, list):
            queryset = Record.objects.filter(pk__in=queryset)
        super(RecordMultipleChoiceField, self).__init__(queryset, **kwargs)


class RecordsWidget(Widget):
    field_class_path = 'formapp.models.RecordMultipleChoiceField'
    widget_class_path = 'autocomplete_light.widgets.MultipleChoiceWidget'

    provides = models.ForeignKey('appstore.AppFeature', null=True)

    class Meta:
        verbose_name = _(u'Relation to other record')
        verbose_name_plural = _(u'Relations to other record')

    def widget_kwargs(self):
        return {
            'autocomplete': 'AutocompleteRecord',
            'autocomplete_js_attributes': {
                'minimum-characters': 0,
            },
            'widget_js_attributes': {
                'bootstrap': 'record-autocomplete',
                'feature': self.provides.pk,
            },
            'extra_context': {
                'feature': self.provides.pk,
            }
        }

    def field_kwargs(self):
        kwargs = super(RecordsWidget, self).field_kwargs()

        # IMPORTANT: this security vulnerability might be used to steal data !
        # Set a self.secure_queryset to avoid this.
        secure_queryset = getattr(self, 'secure_queryset', None)
        if secure_queryset is None:
            raise Exception('Queryset was not secured !')

        kwargs['queryset'] = self.secure_queryset

        if self.provides:
            kwargs['queryset'] = kwargs['queryset'].filter(
                    form__appform__app__provides=self.provides)

        return kwargs
