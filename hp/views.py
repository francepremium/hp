from django import http
from django.core.urlresolvers import reverse
from django.views import generic

from form_designer.models import Form


class CreateGateway(generic.TemplateView):
    template_name = 'add.html'

    @property
    def forms(self):
        forms = getattr(self, '_forms', None)

        if forms is None:
            env = self.request.session['appstore_environment']

            self._forms = Form.objects.filter(appform__app__environment=env,
                    appform__app__deployed=True)

            feature = self.request.GET.get('feature', False)
            if feature:
                self._forms = self._forms.filter(
                        appform__app__provides_id=feature)

        return self._forms

    def get_context_data(self, *args, **kwargs):
        context = super(CreateGateway, self).get_context_data(*args, **kwargs)
        context['forms'] = self.forms
        return context

    def get(self, request, *args, **kwargs):
        if self.forms.count() == 1:
            return http.HttpResponseRedirect(u'%s?is_popup=%s' % (
                reverse('formapp_record_create', args=(self.forms[0].pk,)),
                self.request.GET.get('is_popup', 0)))
        return super(CreateGateway, self).get(request, *args, **kwargs)
