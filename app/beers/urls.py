from django.conf.urls import url
from app.beers.views import BeerSearchJsonView, CreateBeerView

urlpatterns = [
    url(r'^api/search/$', BeerSearchJsonView.as_view(), name='search'),
    url(r'^create/$', CreateBeerView.as_view(), name='create'),
]