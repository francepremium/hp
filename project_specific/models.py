from django.conf import settings
from django.contrib.sites.models import Site

if settings.HOSTNAME == 'maria':
    domain = 'dev.betspire.com'
else:
    domain = 'localhost:8000'
Site.objects.update(domain=domain)
