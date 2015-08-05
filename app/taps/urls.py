from django.conf.urls import url
from app.taps.views import TapListView, TapBeerChangeView, TapEmptyView

urlpatterns = [
    url(r'^list/$', TapListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/change_beer/$', TapBeerChangeView.as_view(), name='change_beer'),
    url(r'^(?P<pk>\d+)/empty/$', TapEmptyView.as_view(), name='empty'),
]
