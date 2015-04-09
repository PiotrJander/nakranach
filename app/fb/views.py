# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.utils.translation import ugettext_lazy as _

from django.http import Http404, HttpResponseRedirect

from .utils import parse_signed_request, get_page_ids, restore_pub_from_session
from .models import Page

class TapsView(View):
    def get(self, request, *args, **kwargs):
        pub, redirect = restore_pub_from_session(request)

        if pub is None:
            raise Http404

        for page_id in get_page_ids(request):
            page = None
            try:
                page = Page.objects.get(page=page_id)
            except Page.DoesNotExist:
                page = Page(page=page_id)

            page.pub = pub
            page.save()

        messages.success(request, _(u'Zakładka "Na Kranach" została dodana do stron(y)'))
        return HttpResponseRedirect(redirect)

    def post(self, request, *args, **kwargs):
        fb_request = parse_signed_request(request.POST.get('signed_request'))

        page_id = fb_request['page']['id']
        page = get_object_or_404(Page, page=page_id)

        return render(request, 'fb/tab.html', {
            'taps': page.pub.taps.all()
        })