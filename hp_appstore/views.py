from django.core.urlresolvers import reverse
from django.views import generic

from appstore.models import App, AppCategory

from forms import AppCreateForm, AppEditForm


class AppEditView(generic.UpdateView):
    model = App
    template_name = 'hp_appstore/app_edit_form.html'
    form_class = AppEditForm


class AppFormEditView(generic.UpdateView):
    model = App
    form_class = AppEditForm



class AppCreateView(generic.CreateView):
    model = App
    template_name = 'form.html'
    form_class = AppCreateForm

    def get_context_data(self, **kwargs):
        context = super(AppCreateView, self).get_context_data(**kwargs)
        context['title'] = u'Create app'
        return context

    def get_success_url(self):
        return reverse('hp_appstore_app_edit', args=(self.object.pk,))
