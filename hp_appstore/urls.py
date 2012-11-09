from django.conf.urls import patterns, include, url

from views import (AppCreateView, AppEditView, AppFormEditView)


urlpatterns = patterns('',
    url(r'app/create/$', AppCreateView.as_view(),
        name='hp_appstore_app_create'),
    url(r'app/(?P<pk>\d+)/edit/$', AppEditView.as_view(),
        name='hp_appstore_app_edit'),
    url(r'app/(?P<pk>\d+)/form/edit/$', AppFormEditView.as_view(),
        name='hp_appstore_app_form_edit'),
)
