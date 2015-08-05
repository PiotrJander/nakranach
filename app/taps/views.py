from django.http import Http404
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import ProcessFormView
from django_tables2.views import SingleTableView
from app.taps.forms import ChangeBeerOnTapForm
from app.taps.tables import TapTable


class TapListView(SingleTableView):
    # model = Profile
    table_class = TapTable
    template_name = 'taps/tap_list.html'

    def get_queryset(self):
        return self.request.profile.get_taps()

    def get_context_data(self, **kwargs):
        context = super(TapListView, self).get_context_data(**kwargs)
        context['change_beer_form'] = ChangeBeerOnTapForm(user=self.request.user)
        return context


class TapProcessFormView(SingleObjectMixin, ProcessFormView):

    def get_object(self, queryset=None):
        try:
            return super(TapProcessFormView, self).get_object(queryset)
        except Http404 as e:
            raise e
            # TODO make user friendly

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(TapProcessFormView, self).post(request, *args, **kwargs)


class TapBeerChangeView(TapProcessFormView):
    pass


class TapEmptyView(TapProcessFormView):
    pass