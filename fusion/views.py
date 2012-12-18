from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.views import generic
from django.utils.translation import ugettext as _

import django_tables2 as tables

from formapp.models import Record, RecordsWidget

from forms import ListForm
from models import List


class LinkedColumn(tables.Column):
    def render(self, value):
        links = []
        for record in Record.objects.filter(pk__in=value):
            links.append(u'<a href="%s">%s</a>' % (
                record.get_absolute_url(), unicode(record)))
        return mark_safe(u', '.join(links))


class RecordColumn(tables.Column):
    def render(self, value):
        return render_to_string('fusion/_record_column.html',
            {'record': value})


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

        table_data = []
        for record in records:
            data = {
                '_record_': record,
            }
            data.update(record.data)
            table_data.append(data)

        columns = {
            '_record_': RecordColumn(),
        }
        for widget in self.object.columns.select_subclasses():
            if isinstance(widget, RecordsWidget):
                columns[widget.name] = LinkedColumn(
                    verbose_name=widget.verbose_name)
            else:
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
