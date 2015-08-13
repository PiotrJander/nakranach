from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect, HttpResponseBadRequest

from django.views.generic.edit import BaseFormView
from django_tables2.views import SingleTableView
from app.pubs.forms import RemoveBeerFromWaitingBeersForm
from braces.views import UserFormKwargsMixin

from app.pubs.tables import WaitingBeersTable


class WaitingBeersTableView(SingleTableView):
    table_class = WaitingBeersTable
    template_name = 'pubs/waiting_beers_list.html'

    def get_queryset(self):
        return self.request.profile.get_pub().waiting_beers.all()


class RemoveBeerFromWaitingBeersView(UserFormKwargsMixin, BaseFormView):
    form_class = RemoveBeerFromWaitingBeersForm
    success_url = reverse_lazy('pub:waiting_beers')

    def form_valid(self, form):
        form.save()
        return super(RemoveBeerFromWaitingBeersView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponseBadRequest()