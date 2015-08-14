from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseBadRequest

from django.views.generic.edit import BaseFormView
from django_tables2.views import SingleTableView
from app.pubs.forms import RemoveBeerFromWaitingBeersForm, ModifyWaitingBeerForm
from braces.views import UserFormKwargsMixin

from app.pubs.tables import WaitingBeersTable


class WaitingBeersTableView(SingleTableView):
    table_class = WaitingBeersTable
    template_name = 'pubs/waiting_beers_list.html'

    def get_queryset(self):
        return self.request.profile.get_pub().waitingbeer_set.all()

    def get_context_data(self, **kwargs):
        context = super(WaitingBeersTableView, self).get_context_data(**kwargs)
        context['modify_waiting_beer_form'] = ModifyWaitingBeerForm(user=self.request.user)
        return context


class EditWaitingBeerViewMixin(UserFormKwargsMixin, BaseFormView):
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