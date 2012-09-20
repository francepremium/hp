from django.conf import settings


def hp_settings(request):
    return dict(DEBUG=settings.DEBUG)
