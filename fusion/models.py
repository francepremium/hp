from django.db import models
from django.db.models import signals
from django.core.urlresolvers import reverse

from form_designer.models import Form, Widget
from appstore.signals import post_app_install


class List(models.Model):
    environment = models.ForeignKey('appstore.Environment')
    feature = models.ForeignKey('appstore.AppFeature')
    columns = models.ManyToManyField('form_designer.Widget')

    def get_absolute_url(self):
        return reverse('fusion_list_detail', args=(self.feature.pk,))


def list_created_initial_columns(sender, instance, created, **kwargs):
    if instance.columns.count() > 0:
        return

    forms = Form.objects.filter(
        appform__app__environment=instance.environment,
        appform__app__provides=instance.feature,
    ).order_by('-pk')

    deployed_forms = forms.filter(appform__app__deployed=True)

    if not deployed_forms.count():
        if not forms.count():
            return

        form = forms[0]
    else:
        form = deployed_forms[0]

    widgets = Widget.objects.filter(tab__form=form).order_by(
        'tab', 'tab__order', 'order')[:5]

    for widget in widgets:
        instance.columns.add(widget)
signals.post_save.connect(list_created_initial_columns, sender=List)
