from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

if settings.HOSTNAME == 'maria':
    domain = 'dev.betspire.com'
else:
    domain = 'localhost:8000'
Site.objects.update(domain=domain)


def name(user):
    if user.first_name and user.last_name:
        return u'%s %s' % (user.first_name, user.last_name)
    elif user.first_name:
        return user.first_name
    elif user.last_name:
        return user.last_name
    elif user.username:
        return user.username
    else:
        return user.email

User.__unicode__ = name
