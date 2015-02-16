from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = format_suffix_patterns([
    url(r'^pubs/$', PubList.as_view(), name='api-pub-list'),
    url(r'^pubs/changes/$', ChangesView.as_view(), name='api-tap-changes'),
    url(r'^pubs/(?P<slug>[a-z0-9-]+)/$', PubView.as_view(), name='api-pub-view'),
    url(r'^pubs/(?P<slug>[a-z0-9-]+)/taps/$', TapList.as_view(), name='api-pub-taps'),
    url(r'^pubs/(?P<slug>[a-z0-9-]+)/changes/$', TapChangeList.as_view(), name='api-pub-tap-changes'),
])