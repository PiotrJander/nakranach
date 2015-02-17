from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<slug>[a-z0-9-]+)/$', PubView.as_view(), name='pub-view')
)
