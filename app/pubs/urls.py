from django.conf.urls import url
from app.pubs.views import WaitingBeersTableView

urlpatterns = [
    url(r'^waiting_beers/$', WaitingBeersTableView.as_view(), name='waiting_beers')
]