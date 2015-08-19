from django.conf.urls import url
from app.beers.views import BeerSearchJsonView

urlpatterns = [
    url(r'^search/$', BeerSearchJsonView.as_view(), name='search'),
]