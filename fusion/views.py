from django.views import generic

import django_tables2 as tables

from formapp.models import Record

from forms import ListForm
from models import List


class RecordTable(tables.Table):
    pass


class ListDetailView(generic.UpdateView):
    model = List
    form_class = ListForm
    template_name = 'fusion/list_detail.html'

    def get_object(self):
        obj, c = List.objects.get_or_create(
            feature_id=self.kwargs['feature_pk'],
            environment=self.request.session['appstore_environment'])

        return obj

    def get_context_data(self, **kwargs):
        q = self.request.GET.get('q', None)
        if q:
            records = Record.objects.search(q)
        else:
            records = Record.objects.all()

        records = records.filter(
            environment=self.request.session['appstore_environment'],
            form__appform__app__provides_id=self.kwargs['feature_pk'])

        table_data = [record.data for record in records]

        columns = {}
        for widget in self.object.columns.all():
            columns[widget.name] = tables.Column(
                verbose_name=widget.verbose_name)

        for name in columns.keys():
            for data in table_data:
                if name not in data:
                    data[name] = None

        table_class = type('RecordTable', (RecordTable,), columns)

        context = super(ListDetailView, self).get_context_data(**kwargs)

        table = table_class(table_data)
        tables.RequestConfig(self.request).configure(table)
        context['table'] = table

        return context
