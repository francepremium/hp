from django.db import models
from django.db.models.signals import pre_save

import jsonfield
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField

from form_designer.models import Widget


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

    @property
    def feature(self):
        return self.form.appform.app.provides


def text_data(sender, instance, **kwargs):
    instance.text_data = u''.join(
        [unicode(x) for x in instance.data.values() if x])
pre_save.connect(text_data, sender=Record)


class RelationWidget(Widget):
    field_class_path = 'django.forms.models.ModelMultipleChoiceField'
    widget_class_path = 'autocomplete_light.widgets.MultipleChoiceWidget'

    provides = models.ForeignKey('appstore.AppFeature', null=True, blank=True)
    maximum_values = models.IntegerField()

    def widget_kwargs(self):
        return {
            'autocomplete': 'AutocompleteRecord',
        }

    def field_kwargs(self):
        kwargs = super(RelationWidget, self).field_kwargs()

        # TODO: Secure this based on session[appstore_environment]
        # IMPORTANT: this security vulnerability might be used to steal data !
        kwargs['queryset'] = Record.objects.all()

        if self.provides:
            kwargs['queryset'] = kwargs['queryset'].filter(
                    form__appform__app__provides=self.provides)

        return kwargs
