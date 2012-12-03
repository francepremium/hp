from django.views import generic

from appstore.contrib.form_designer_appeditor.models import AppForm


class AppPkFormClassMixin(object):
    def get_form_class(self):
        self.appform = AppForm.objects.get(app__pk=self.kwargs['app_pk'],
                                           app__deployed=True)
        return self.appform.form.get_form_class()


class Create(AppPkFormClassMixin, generic.FormView):
    template_name = 'formapp/form.html'

    def get_context_data(self, **kwargs):
        context = super(Create, self).get_context_data(**kwargs)
        context['appform'] = self.appform
        return context


class Update(AppPkFormClassMixin, generic.FormView):
    template_name = 'formapp/form.html'


class List(generic.TemplateView):
    template_name = 'formapp/list.html'


class Detail(generic.TemplateView):
    template_name = 'formapp/detail.html'


class Delete(generic.TemplateView):
    template_name = 'formapp/detele.html'
