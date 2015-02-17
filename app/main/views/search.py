from django.http import HttpResponse
from django.views.generic import View

from haystack.query import SearchQuerySet

import json

class AutocompleteView(View):
    def get(self, request):
        q = request.GET.get('q', '')

        sqs = SearchQuerySet().autocomplete(content_auto=q)

        data = [object.name for object in sqs]

        response = json.dumps({
            'results': data
        })

        return HttpResponse(response, content_type='application/json')