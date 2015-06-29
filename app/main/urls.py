from django.core.urlresolvers import reverse
from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout
from django.views.generic.base import View

from haystack.views import SearchView, search_view_factory
from haystack.forms import HighlightedModelSearchForm

from .views import *
from .views.landing import landing

urlpatterns = patterns('',
    # url(r'^$', IndexView.as_view(), name='index'),
    url(r'^$', landing, name='landing'),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'^dummy/$', View.as_view(), name='dummy'),

    url(r'pubs/search/$', search_view_factory(
        form_class=HighlightedModelSearchForm,
        view_class=SearchView,
        template='search/pubs.html',
        results_per_page=10
    ), name='pubs-search'),
    url(r'pubs/search/autocomplete/$', AutocompleteView.as_view(), name='autocomplete'),
    url(r'^(?P<slug>[a-z0-9-]+)/$', PubView.as_view(), name='pub-view')
)
