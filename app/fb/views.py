from django.views.generic import View

from django.http import HttpResponse

class TapsView(View):
    def get(self, request, *args, **kwargs):
        print request.POST
        return HttpResponse('test')

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)