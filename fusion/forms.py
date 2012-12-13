from django import forms

from form_designer.models import Widget

from models import List


class ListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)

        obj = kwargs['instance']

        widgets = Widget.objects.filter(
            tab__form__appform__app__provides=obj.feature,
            tab__form__appform__app__environment=obj.environment).distinct()
        widgets = {w.name: w for w in widgets}

        self.fields['columns'].queryset = Widget.objects.filter(pk__in=
            [w.pk for w in widgets.values()])

    class Meta:
        model = List
        fields = ('columns',)
