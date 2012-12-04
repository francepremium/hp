from django.db.models.signals import post_syncdb
from django.conf import settings
import django.contrib.sites.models
from django.contrib.sites.models import Site

import appstore.models
from appstore.models import AppFeature


def appfeature(sender, **kwargs):
    for name in ('other', 'artist', 'artwork', 'contact'):
        AppFeature.objects.get_or_create(name=name)
post_syncdb.connect(appfeature, sender=appstore.models)


def site(sender, **kwargs):
    if settings.HOSTNAME == 'maria':
        domain = 'dev.betspire.com'
    else:
        domain = 'localhost:8000'
    Site.objects.update(domain=domain)
post_syncdb.connect(site, sender=django.contrib.sites.models)
