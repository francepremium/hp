from django.db import models

from djorm_hstore.models import HStoreManager
from djorm_hstore.fields import DictionaryField

from form_designer.models import Widget


class Record(models.Model):
    form = models.ForeignKey('form_designer.Form')
    environment = models.ForeignKey('appstore.Environment')

    data = DictionaryField(db_index=True)

    @property
    def feature(self):
        return self.form.appform.app.provides


class RelationWidget(Widget):
    field_class_path = 'django.forms.models.ModelMultipleChoiceField'
    widget_class_path = 'django.forms.widgets.SelectMultiple'

    provides = models.ForeignKey('appstore.AppFeature', null=True, blank=True)
    maximum_values = models.IntegerField()

    def field_kwargs(self):
        kwargs = super(RelationWidget, self).field_kwargs()
        kwargs['queryset'] = Record.objects.all()
        if self.provides:
            kwargs['queryset'] = kwargs['queryset'].filter(
                    form__appform__app__provides=self.provides)
        return kwargs
