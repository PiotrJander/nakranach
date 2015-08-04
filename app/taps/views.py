from django_tables2.views import SingleTableView
from app.taps.tables import TapTable


class TapListView(SingleTableView):
    # model = Profile
    table_class = TapTable
    template_name = 'taps/tap_list.html'

    def get_queryset(self):
        return self.request.profile.get_pub().get_taps()