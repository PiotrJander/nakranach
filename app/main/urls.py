from django.conf.urls import patterns, url

from haystack.views import SearchView, search_view_factory
from haystack.forms import HighlightedModelSearchForm

from .views import *
from .views.landing import landing

urlpatterns = patterns('',
    # url(r'^$', IndexView.as_view(), name='index'),
    url(r'^$', landing, name='landing'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout', kwargs={'next_page': '/login/'}),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard'),
    url(r'pubs/search/$', search_view_factory(
        form_class=HighlightedModelSearchForm,
        view_class=SearchView,
        template='search/pubs.html',
        results_per_page=10
    ), name='pubs-search'),
    url(r'pubs/search/autocomplete/$', AutocompleteView.as_view(), name='autocomplete'),
    url(r'^(?P<slug>[a-z0-9-]+)/$', PubView.as_view(), name='pub-view')
)
