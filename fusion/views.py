import json

from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
from django.views import generic
from django.utils.translation import ugettext as _
from django import http

import django_tables2 as tables

from form_designer.models import Widget
from formapp.models import Record, RecordsWidget

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


class ListDetailView(generic.DetailView):
    model = List
    template_name = 'fusion/list_detail.html'

    def get_object(self):
        obj, c = List.objects.get_or_create(
            feature_id=self.kwargs['feature_pk'],
            environment=self.request.session['appstore_environment'])

        return obj

    def get_context_data(self, **kwargs):
        q = self.request.GET.get('q', None)
        if q:
            if '*' in q:
                q = q.replace('*', '')
                records = Record.objects.filter(text_data__icontains=q)
            else:
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

            for k, v in data.items():
                if isinstance(v, basestring) and v.isdigit():
                    data[k] = int(v)

            table_data.append(data)

        columns = {
            '_record_': RecordColumn(),
        }


        widgets_qs = Widget.objects.filter(
            tab__form__appform__app__provides=self.object.feature,
            tab__form__appform__app__environment=self.object.environment).distinct()
        widgets_qs = Widget.objects.filter(pk__in=widgets_qs.values_list('pk')
                                           ).order_by('tab', 'tab__order')

        list_columns = ListColumn.objects.filter(list=self.object)

        for column in list_columns:
            widget = column.widget.type_cast()
            attrs = {
                'th': {
                    'data-widget-pk': widget.widget_ptr_id,
                    'data-widget-name': widget.name,
                }
            }

            if isinstance(widget, RecordsWidget):
                columns[widget.name] = LinkedColumn(
                    verbose_name=widget.verbose_name,
                    attrs=attrs)
            else:
                columns[widget.name] = tables.Column(
                    verbose_name=widget.verbose_name,
                    attrs=attrs)

            widgets_qs = widgets_qs.exclude(name=widget.name)

        for name in columns.keys():
            for data in table_data:
                if name not in data:
                    data[name] = None

        table_class = type('RecordTable', (RecordTable,), columns)

        context = super(ListDetailView, self).get_context_data(**kwargs)

        table = table_class(table_data)
        tables.RequestConfig(self.request).configure(table)
        context['table'] = table
        context['widgets'] = widgets_qs

        return context


class ListUpdateView(generic.DetailView):
    model = List

    def get_object(self):
        obj = super(ListUpdateView, self).get_object()

        if obj.environment != self.request.session['appstore_environment']:
            return None

        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if not self.object:
            raise http.HttpResponseForbidden()

        data = json.loads(request.POST.get('data', '[]'))
        remove = request.POST.get('remove', None)
        add = request.POST.get('add', None)

        if data:
            order = 0
            for column_data in data['columns']:
                lc, c = ListColumn.objects.get_or_create(
                    list=self.object, widget__pk=column_data['widget_pk'])

                lc.order = order
                lc.save()

                order += 1
        elif remove:
            ListColumn.objects.get(widget__pk=remove, list=self.object
                ).delete()
        elif add:
            ListColumn.objects.create(widget=Widget.objects.get(pk=add),
                list=self.object, order=100)

        return http.HttpResponse('')
