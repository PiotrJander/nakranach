from django.conf.urls import url
from app.pubs.views import WaitingBeersTableView, RemoveBeerFromWaitingBeersView, ModifyWaitingBeerView

urlpatterns = [
    url(r'^waiting/$', WaitingBeersTableView.as_view(), name='waiting_beers'),
    url(r'^remove/$', RemoveBeerFromWaitingBeersView.as_view(), name='remove_beer'),
    url(r'^modify/$', ModifyWaitingBeerView.as_view(), name='modify_beer'),
]