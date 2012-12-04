import autocomplete_light

from models import Record


class AutocompleteRecord(autocomplete_light.AutocompleteModelBase):
    search_fields = ['..']

    def choices_for_values(self):
        for ctype, pk in self.values:
            if ctype != [u'formapp', u'record']:
                raise Exception('Not implemented: multiple ctype')

        # TODO: secure here
        choices = Record.objects.filter(pk__in=[pk for c, pk in self.values])

        return choices

    def choices_for_request(self):
        q = self.request.GET.get('q', '')
        exclude = self.request.GET.getlist('exclude', [])

        if q:
            choices = Record.objects.search(q)
        else:
            choices = Record.objects.all()

        choices = choices.filter(
            environment=self.request.session['appstore_environment'])

        return self.order_choices(choices).exclude(pk__in=exclude
            )[0:self.limit_choices]
autocomplete_light.register(Record, AutocompleteRecord, name='AutocompleteRecord')
