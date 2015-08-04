from django.conf.urls import url
from app.taps.views import TapListView

urlpatterns = [
    url(r'^list/$', TapListView.as_view(), name='list'),
]
