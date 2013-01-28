from itertools import chain

from django import forms
from django.utils.encoding import force_unicode
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from form_designer.models import Widget

from models import List


class WidgetsSelectWidget(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<ul>']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])

        previous_tab = None
        for i, (option_value, option_label) in enumerate(chain(self.choices, choices)):
            model = self.choices.queryset[i]

            if model.tab != previous_tab:
                if previous_tab is not None:
                    output.append('</li></ul>')
                output.append('<li>')
                output.append(model.tab.verbose_name)
                output.append('<ul>')

            previous_tab = model.tab

            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = forms.CheckboxInput(final_attrs, check_test=lambda value:
                                     value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))
        output.append(u'</ul>')
        return mark_safe(u'\n'.join(output))


class ListForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)

        obj = kwargs['instance']

        widgets_qs = Widget.objects.filter(
            tab__form__appform__app__provides=obj.feature,
            tab__form__appform__app__environment=obj.environment).order_by(
                'tab__order')

        self.fields['columns'].queryset = widgets_qs
        self.fields['columns'].help_text = u''

    class Meta:
        model = List
        fields = ('columns',)
        widgets = {'columns': WidgetsSelectWidget}
