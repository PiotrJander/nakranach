from django_tables2.views import SingleTableView
from app.pubs.tables import WaitingBeersTable


class WaitingBeersTableView(SingleTableView):
    table_class = WaitingBeersTable
    template_name = 'pubs/waiting_beers_list.html'

    def get_queryset(self):
        return self.request.profile.get_pub().waiting_beers.all()
