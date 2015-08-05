from braces.views import UserFormKwargsMixin
from django.views.generic.edit import FormMixin
from django_tables2.views import SingleTableView
from app.taps.forms import ChangeBeerOnTapForm
from app.taps.tables import TapTable


class TapListView(UserFormKwargsMixin, FormMixin, SingleTableView):
    # model = Profile
    table_class = TapTable
    template_name = 'taps/tap_list.html'
    form_class = ChangeBeerOnTapForm

    def get_queryset(self):
        return self.request.profile.get_pub().get_taps()

    def get_context_data(self, **kwargs):
        context = super(TapListView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
