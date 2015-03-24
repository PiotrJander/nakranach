from django.conf.urls import url, include

from rest_framework.urlpatterns import format_suffix_patterns

from .views import *

urlpatterns = format_suffix_patterns([
    url(r'^auth/login/$', Login.as_view(), name='api-authenticate'),
    url(r'^auth/facebook/$', FacebookAuthenticate.as_view(), name='api-facebook-authenticate'),
    url(r'^auth/logout/$', Logout.as_view(), name='api-logout'),
    url(r'^auth/register/$', Register.as_view(), name='api-register'),

    url(r'^changes/$', ChangesView.as_view(), name='api-tap-changes'),
    url(r'^pubs/$', PubList.as_view(), name='api-pub-list'),
    url(r'^pubs/nearest/$', NearestPubsView.as_view(), name='api-nearest-pubs'),
    url(r'^pubs/(?P<slug>[a-z0-9-]+)/$', PubView.as_view(), name='api-pub-view'),
    url(r'^pubs/(?P<slug>[a-z0-9-]+)/taps/$', TapList.as_view(), name='api-pub-taps'),
    url(r'^pubs/(?P<slug>[a-z0-9-]+)/changes/$', TapChangeList.as_view(), name='api-pub-tap-changes'),
])