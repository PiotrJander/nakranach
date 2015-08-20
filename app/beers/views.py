import json

from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponse
from django.views import generic
from django_tables2 import SingleTableMixin
from braces.views import UserFormKwargsMixin

from app.beers.forms import CreateBeerForm
from app.beers.models import Beer
from app.beers.tables import BeersTable
from app.main.utils import normalize_for_search
from app.main.viewmixins import CanManageWaitingBeersMixin


class BeerSearchJsonView(generic.View):
    """
    ``BeerSearchJsonView`` view uses the ``q`` GET parameter to filter ``Beer``s. It then returns a JSON response
    which has a list of dicts, where a dict represents a Beer and has keys: ``name``, ``brewery``,
    and ``secondary_data``.
    """
    def get(self, request):
        q = request.GET['q']
        querystring = normalize_for_search(q)
        beers = Beer.match(querystring)
        beer_dict_list = [beer.search_dict() for beer in beers]
        jsonified = json.dumps(beer_dict_list)
        return HttpResponse(jsonified, content_type='application/json')
        # TODO test


class CreateBeerView(CanManageWaitingBeersMixin, SingleTableMixin, UserFormKwargsMixin, generic.edit.FormView):
    table_class = BeersTable
    template_name = 'beers/create_beer.html'
    form_class = CreateBeerForm
    success_url = reverse_lazy('pub:waiting_beers')

    def get_queryset(self):
        return Beer.objects.all()

    def get_context_data(self, **kwargs):
        context = super(CreateBeerView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def form_valid(self, form):
        form.save()
        return super(CreateBeerView, self).form_valid(form)
