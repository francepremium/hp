from django.core.urlresolvers import reverse
from django.views import generic
from django import http

import rules_light

from appstore.views import AppCreateView
from appstore.contrib.form_designer_appeditor.models import AppForm

from forms import RecordForm
from models import Record


class AppCreateOverride(AppCreateView):
    def get_success_url(self):
        return reverse('form_designer_appeditor_appform_update',
                args=(self.object.pk,))


class FormRedirectMixin(object):
    def get_success_url(self, record):
        if '_continue' in self.request.POST.keys():
            return reverse('formapp_record_update', args=(record.pk,))
        elif '_another' in self.request.POST.keys():
            return reverse('formapp_record_create',
                    args=(record.form.appform.app.pk,))

class Create(FormRedirectMixin, generic.CreateView):
    template_name = 'formapp/record_form.html'

    @property
    def appform(self):
         return AppForm.objects.get(app__pk=self.kwargs['app_pk'],
                 app__deployed=True)

    def get_form_class(self):
        return self.appform.form.get_form_class(bases=(RecordForm,))

    def get_context_data(self, **kwargs):
        rules_light.require(self.request.user, 'formapp.record.create')

        context = super(Create, self).get_context_data(**kwargs)
        context['appform'] = self.appform
        return context

    def form_valid(self, form):
        record = form.save(self, commit=False)
        record.form = self.appform.form
        record.environment = self.request.session['appstore_environment']
        record.save()
        return http.HttpResponseRedirect(self.get_success_url(record))


class Update(FormRedirectMixin, generic.UpdateView):
    model = Record

    @property
    def appform(self):
        return self.object.form.appform

    def get_queryset(self):
        # basic, annoying security for now.
        return Record.objects.filter(
            environment=self.request.session['appstore_environment'])

    def get_context_data(self, **kwargs):
        context = super(Update, self).get_context_data(**kwargs)
        context['appform'] = self.appform
        return context

    def get_form_class(self):
        return self.object.form.get_form_class(bases=(RecordForm,))

    def form_valid(self, form):
        record = form.save(self)
        return http.HttpResponseRedirect(self.get_success_url(record))


class Search(generic.ListView):
    def get_queryset(self):
        rules_light.require(self.request.user, 'formapp.record.list')

        q = self.request.GET.get('q', None)

        if q:
            records = Record.objects.search(q)
        else:
            records = Record.objects.all()

        return records.filter(
            environment=self.request.session['appstore_environment'])


class List(generic.ListView):
    def get_queryset(self):
        rules_light.require(self.request.user, 'formapp.record.list')

        return Record.objects.filter(
            form__appform__app__provides__pk=self.kwargs['feature_pk'],
            environment=self.request.session['appstore_environment'])

    def get_context_data(self, **kwargs):
        context = super(List, self).get_context_data(**kwargs)
        return context


@rules_light.class_decorator
class Detail(generic.TemplateView):
    template_name = 'formapp/detail.html'


@rules_light.class_decorator
class Delete(generic.TemplateView):
    template_name = 'formapp/detele.html'
