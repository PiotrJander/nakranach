import json
from django.http.response import HttpResponse
from django.views import generic
from app.beers.models import Beer
from app.main.utils import normalize_for_search


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
        beer_dict_list = (beer.search_dict() for beer in beers)
        jsonified = json.dumps(beer_dict_list)
        return HttpResponse(jsonified, content_type='application/json')
        # TODO test