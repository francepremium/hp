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
    Site.objects.update(domain=settings.SITE_DOMAIN, name=settings.SITE_NAME)
post_syncdb.connect(site, sender=django.contrib.sites.models)
