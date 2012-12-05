from django import forms
from django.contrib.contenttypes.models import ContentType

from models import Record, RecordsWidget, Widget


class RecordForm(forms.Form):
    def __init__(self, instance=None, *args, **kwargs):
        if instance is None:
            self.instance = Record()
        else:
            self.instance = instance
            kwargs['initial'] = self.instance.data

        super(RecordForm, self).__init__(*args, **kwargs)

    def save(self, view, commit=True):
        data = {}

        widgets = Widget.objects.filter(tab__form=view.appform.form
                ).select_subclasses()
        widgets = {w.name: w for w in widgets}

        for key, value in self.cleaned_data.items():
            if isinstance(widgets[key], RecordsWidget):
                value = [v.pk for v in value]

            #if value and hasattr(value, '__iter__'):
            #    ct = ContentType.objects.get_for_model(value.model)
            #    value = [(ct.natural_key(), v.pk) for v in value]

            data[key] = value

        self.instance.data = data

        if commit:
            self.instance.save()

        return self.instance
