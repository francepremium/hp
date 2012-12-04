from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    url(r'list/$',
        views.List.as_view(),
        name='formapp_record_list'),
    url(r'(?P<app_pk>\d+)/create/$',
        views.Create.as_view(),
        name='formapp_record_create'),
    url(r'(?P<pk>\d+)/update/$',
        views.Update.as_view(),
        name='formapp_record_update'),
#    url(r'(?P<uuid>' + UUID_REGEXP + ')/detail$',
#        views.Detail.as_view(),
#        name='formapp_record_detail'),
    url(r'(?P<pk>\d+)/delete/$',
        views.Delete.as_view(),
        name='formapp_record_delete'),
)
