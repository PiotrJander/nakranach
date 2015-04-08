from django.views.generic import View

from django.http import HttpResponse

from .utils import parse_signed_request

class TapsView(View):
    def get(self, request, *args, **kwargs):
        print parse_signed_request(request.POST.get('signed_request'))

        return HttpResponse('test')

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)