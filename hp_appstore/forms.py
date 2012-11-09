from django import forms

import autocomplete_light
from autocomplete_light.contrib.taggit_tagfield import TagField, TagWidget

from appstore.models import App


class AppCreateForm(forms.ModelForm):
    class Meta:
        model = App
        exclude = ('fork_of',)
        widgets = {
            'tags': autocomplete_light.TextWidget('TagAutocomplete'),
        }


class AppEditForm(forms.ModelForm):
    tags = TagField(widget=TagWidget('TagAutocomplete'))

    class Meta:
        model = App
        exclude = ('fork_of', 'default_for_feature', 'provides')
