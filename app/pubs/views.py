from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.views.generic.base import View
from django.views.generic.edit import BaseFormView
from django_tables2.views import SingleTableView
from braces.views import UserFormKwargsMixin
from app.beers.forms import CreateBeerForm
from app.main.viewmixins import CanManageWaitingBeersMixin

from app.pubs.forms import RemoveBeerFromWaitingBeersForm, ModifyWaitingBeerForm, DatabaseBeerDisabledForm, \
    AddWaitingBeerForm
from app.pubs.tables import WaitingBeersTable


class WaitingBeersTableView(CanManageWaitingBeersMixin, SingleTableView):
    table_class = WaitingBeersTable
    template_name = 'pubs/waiting_beers_list.html'

    def get_queryset(self):
        return self.request.profile.get_pub().waitingbeer_set.all()

    def get_context_data(self, **kwargs):
        context = super(WaitingBeersTableView, self).get_context_data(**kwargs)
        context.update({
            'modify_waiting_beer_form': ModifyWaitingBeerForm(user=self.request.user),
            'database_beer_disabled_form': DatabaseBeerDisabledForm(),
            'create_beer_form': CreateBeerForm(user=self.request.user),
        })
        return context

class EditWaitingBeerViewMixin(CanManageWaitingBeersMixin, UserFormKwargsMixin, BaseFormView):
    success_url = reverse_lazy('pub:waiting_beers')

    def form_valid(self, form):
        form.save()
        return super(EditWaitingBeerViewMixin, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponseBadRequest()


class RemoveBeerFromWaitingBeersView(EditWaitingBeerViewMixin):
    form_class = RemoveBeerFromWaitingBeersForm


class ModifyWaitingBeerView(EditWaitingBeerViewMixin):
    form_class = ModifyWaitingBeerForm


class AddWaitingBeerView(EditWaitingBeerViewMixin):
    form_class = AddWaitingBeerForm


class WaitingBeerJsonView(CanManageWaitingBeersMixin, View):
    def get(self, request):
        pub = request.profile.get_pub()
        waitingbeer = pub.waitingbeer_set.get(id=request.GET['id'])
        return JsonResponse(waitingbeer.export_form_data_with_beer())