from django.views import generic
from django import http

from models import Record
from appstore.contrib.form_designer_appeditor.models import AppForm


class Create(generic.FormView):
    template_name = 'formapp/record_form.html'

    def get_form_class(self):
        self.appform = AppForm.objects.get(app__pk=self.kwargs['app_pk'],
                                           app__deployed=True)
        return self.appform.form.get_form_class()

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        context['appform'] = self.appform
        return context

    def form_valid(self, form):
        record = Record.objects.create(form=self.appform.form,
            environment=self.request.session['appstore_environment'],
            data=form.cleaned_data)
        return http.HttpResponseRedirect(self.request.path)


class Update(generic.UpdateView):
    model = Record

    def get_context_data(self, **kwargs):
        context = super(Update, self).get_context_data(**kwargs)
        context['appform'] = self.object.form.appform
        return context

    def get_form_class(self):
        return self.object.form.get_form_class()

    def get_initial(self):
        return self.object.data

    def get_form_kwargs(self):
        kwargs = super(Update, self).get_form_kwargs()
        kwargs.pop('instance')
        return kwargs

    def form_valid(self, form):
        self.object.data = form.cleaned_data
        self.object.save()
        return http.HttpResponseRedirect(self.request.path)


class List(generic.ListView):
    def get_queryset(self):
        return Record.objects.filter(
            environment=self.request.session['appstore_environment'])


class Detail(generic.TemplateView):
    template_name = 'formapp/detail.html'


class Delete(generic.TemplateView):
    template_name = 'formapp/detele.html'
