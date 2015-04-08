from django.views.generic import View

from django.http import HttpResponse, Http404

from .utils import parse_signed_request, get_page_ids, restore_pub_from_session

class TapsView(View):
    def get(self, request, *args, **kwargs):
        pub = restore_pub_from_session(request)

        if pub is None:
            raise Http404

        print pub

        for page_id in get_page_ids(request):
            print page_id

        return HttpResponse('asdfg')

    def post(self, request, *args, **kwargs):
        print parse_signed_request(request.POST.get('signed_request'))
        return HttpResponse('test')