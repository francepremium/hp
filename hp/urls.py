from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

import autocomplete_light
autocomplete_light.autodiscover()

# override pinax accounts app's signup url
from hp_saas.views import SignupView, LoginView, ConfirmEmailView

from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'homepage.html'}, name='home'),
    # override pinax accounts app's signup url
    url(r'^account/signup/$', SignupView.as_view()),
    url(r'^account/login/$', LoginView.as_view()),
    url(r'^account/confirm_email/(?P<key>\w+)/$', ConfirmEmailView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^session_security/', include('session_security.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^autocomplete_light/', include('autocomplete_light.urls')),
    url(r'^appstore/', include('appstore.urls')),
    url(r'^form_designer/', include('form_designer.urls')),
    url(r'^form_designer_appeditor/',
        include('appstore.contrib.form_designer_appeditor.urls')),
)

# serve static in dev
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
