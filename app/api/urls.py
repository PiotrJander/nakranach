from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = format_suffix_patterns([
    url(r'^pubs/$', PubList.as_view(), name='pub-list'),
    url(r'^pubs/(?P<pk>\d+)/$', PubView.as_view(), name='pub-view'),
    url(r'^pubs/(?P<pk>\d+)/taps/$', TapList.as_view(), name='pub-taps'),
    url(r'^pubs/(?P<pk>\d+)/changes/$', TapChangeList.as_view(), name='pub-tap-changes')
])