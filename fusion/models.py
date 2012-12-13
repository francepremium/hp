from django.db import models
from django.db.models import signals
from django.core.urlresolvers import reverse

from appstore.signals import post_app_install


class List(models.Model):
    environment = models.ForeignKey('appstore.Environment')
    feature = models.ForeignKey('appstore.AppFeature')
    columns = models.ManyToManyField('form_designer.Widget')

    def get_absolute_url(self):
        return reverse('fusion_list_detail', args=(self.feature.pk,))
