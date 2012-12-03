from django.conf.urls import patterns, url

from zodb_light import UUID_REGEXP

import views


urlpatterns = patterns('',
    url(r'(?P<app_pk>\d+)/list/$',
        views.List.as_view(),
        name='formapp_list'),
    url(r'(?P<app_pk>\d+)/create/$',
        views.Create.as_view(),
        name='formapp_create'),
    url(r'(?P<uuid>' + UUID_REGEXP + ')/update/$',
        views.Update.as_view(),
        name='formapp_update'),
    url(r'(?P<uuid>' + UUID_REGEXP + ')/detail$',
        views.Detail.as_view(),
        name='formapp_detail'),
    url(r'(?P<uuid>' + UUID_REGEXP + ')/delete/$',
        views.Delete.as_view(),
        name='formapp_delete'),
)
