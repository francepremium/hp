import autocomplete_light

from models import Record


class AutocompleteRecord(autocomplete_light.AutocompleteModelBase):
    search_fields = ['..']

    def choices_for_request(self):
        q = self.request.GET.get('q', '')
        exclude = self.request.GET.getlist('exclude', [])

        if q:
            choices = Record.objects.filter(text_data__icontains=q)
        else:
            choices = Record.objects.all()

        choices = choices.filter(
            environment=self.request.session['appstore_environment'])

        return self.order_choices(choices).exclude(pk__in=exclude
            )[0:self.limit_choices]
autocomplete_light.register(Record, AutocompleteRecord, name='AutocompleteRecord')
