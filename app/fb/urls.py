from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = patterns('',
    url(r'^$', csrf_exempt(TapsView.as_view()), name='fb-taps')
)