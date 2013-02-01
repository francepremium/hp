from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    url(r'(?P<pk>\d+)/update/$',
        views.ListUpdateView.as_view(),
        name='fusion_list_update'),
    url(r'(?P<feature_pk>\d+)/$',
        views.ListDetailView.as_view(),
        name='fusion_list_detail'),
)
