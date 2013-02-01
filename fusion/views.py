import json

from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.views import generic
from django.utils.translation import ugettext as _
from django import http

import django_tables2 as tables

from formapp.models import Record, RecordsWidget

from forms import ListForm
from models import List, ListColumn


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
            records = Record.objects.filter(text_data__icontains=q)
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

        list_columns = ListColumn.objects.filter(list=self.object)

        for column in list_columns:
            widget = column.widget.type_cast()
            attrs = {
                'th': {'data-widget-pk': widget.widget_ptr_id}
            }

            if isinstance(widget, RecordsWidget):
                columns[widget.name] = LinkedColumn(
                    verbose_name=widget.verbose_name,
                    attrs=attrs)
            else:
                columns[widget.name] = tables.Column(
                    verbose_name=widget.verbose_name,
                    attrs=attrs)

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


class ListUpdateView(generic.DetailView):
    model = List

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        data = json.loads(request.POST['data'])

        order = 0
        for column_data in data['columns']:
            lc, c = ListColumn.objects.get_or_create(
                list=self.object, widget__pk=column_data['widget_pk'])

            lc.order = order
            lc.save()

            order += 1

        return http.HttpResponse('')
