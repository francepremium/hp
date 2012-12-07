from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

import rules_light
rules_light.autodiscover()

import autocomplete_light
autocomplete_light.autodiscover()

# override pinax accounts app's signup url
from hp_saas.views import SignupView, LoginView, ConfirmEmailView
from views import CreateGateway
from formapp.views import AppCreateOverride

from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'homepage.html'}, name='home'),
    url(r'^design/$', direct_to_template, {'template': 'design.html'}, name='design'),
    # override pinax accounts app's signup url
    url(r'^add/$', CreateGateway.as_view(), name='create_gateway'),
    url(r'^account/signup/$', SignupView.as_view()),
    url(r'^account/login/$', LoginView.as_view()),
    url(r'^account/confirm_email/(?P<key>\w+)/$', ConfirmEmailView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^session_security/', include('session_security.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^autocomplete_light/', include('autocomplete_light.urls')),
    url(r'^appstore/app/create/', AppCreateOverride.as_view(), name='appstore_app_create'),
    url(r'^appstore/', include('appstore.urls')),
    url(r'^formapp/', include('formapp.urls')),
    url(r'^form_designer/', include('form_designer.urls')),
    url(r'^form_designer_appeditor/',
        include('appstore.contrib.form_designer_appeditor.urls')),
)

# serve static in dev
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
