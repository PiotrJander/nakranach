from django.conf.urls import url
from app.pubs.views import WaitingBeersTableView, RemoveBeerFromWaitingBeersView

urlpatterns = [
    url(r'^waiting_beers/$', WaitingBeersTableView.as_view(), name='waiting_beers'),
    url(r'^remove_beer/$', RemoveBeerFromWaitingBeersView.as_view(), name='remove_beer'),
]