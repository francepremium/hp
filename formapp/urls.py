from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

import views


urlpatterns = patterns('',
    url(r'search/$',
        login_required(views.Search.as_view()),
        name='formapp_record_search'),
    url(r'(?P<feature_pk>\d+)/list/$',
        login_required(views.List.as_view()),
        name='formapp_record_list'),
    url(r'(?P<app_pk>\d+)/create/$',
        login_required(views.Create.as_view()),
        name='formapp_record_create'),
    url(r'(?P<pk>\d+)/update/$',
        login_required(views.Update.as_view()),
        name='formapp_record_update'),
    url(r'(?P<pk>\d+)/detail/$',
        login_required(views.Detail.as_view()),
        name='formapp_record_detail'),
    url(r'(?P<pk>\d+)/delete/$',
        login_required(views.Delete.as_view()),
        name='formapp_record_delete'),
)
