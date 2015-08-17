from django.conf.urls import url
from app.pubs.views import WaitingBeersTableView, RemoveBeerFromWaitingBeersView, ModifyWaitingBeerView, \
    WaitingBeerJsonView

urlpatterns = [
    url(r'^waiting/$', WaitingBeersTableView.as_view(), name='waiting_beers'),
    url(r'^remove/$', RemoveBeerFromWaitingBeersView.as_view(), name='remove_beer'),
    url(r'^modify/$', ModifyWaitingBeerView.as_view(), name='modify_beer'),
    url(r'^api/beer/$', WaitingBeerJsonView.as_view(), name='waiting_beer_data')
]