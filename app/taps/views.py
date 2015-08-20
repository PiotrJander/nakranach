from braces.views import UserFormKwargsMixin
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.http.response import HttpResponseRedirect
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import FormMixin
from django_tables2.views import SingleTableView

from app.beers.models import Beer
from app.main.viewmixins import CanManageTapsMixin
from app.pubs.models import Tap
from app.taps.forms import ChangeBeerForm
from app.taps.models import TapChange
from app.taps.tables import TapTable


class TapListView(CanManageTapsMixin, SingleTableView):
    table_class = TapTable
    template_name = 'taps/tap_list.html'

    def get_queryset(self):
        return self.request.profile.get_taps()

    def get_context_data(self, **kwargs):
        context = super(TapListView, self).get_context_data(**kwargs)
        context['change_beer_form'] = ChangeBeerForm(user=self.request.user)
        return context


class TapProcessFormView(CanManageTapsMixin, BaseDetailView):
    model = Tap

    def get_object(self, queryset=None):
        try:
            return super(TapProcessFormView, self).get_object(queryset)
        except Http404 as e:
            raise e

    def get_queryset(self):
        return self.request.profile.get_taps()


class TapBeerChangeView(UserFormKwargsMixin, FormMixin, TapProcessFormView):
    form_class = ChangeBeerForm
    success_url = reverse_lazy('tap:list')

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        self.tap = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        new_beer = Beer.objects.get(pk=form.cleaned_data['new_beer'])
        TapChange.log(self.tap, self.tap.beer, new_beer, self.request.profile)
        self.tap.change_beer(new_beer)
        return super(TapBeerChangeView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_success_url())


class TapEmptyView(TapProcessFormView):

    def post(self, request, *args, **kwargs):
        tap = self.get_object()
        TapChange.log(tap, tap.beer, None, self.request.profile)
        tap.empty()
        return HttpResponseRedirect(reverse_lazy('tap:list'))