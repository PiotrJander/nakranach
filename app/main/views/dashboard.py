from django.views.generic import TemplateView

from ..sidebar_utils import SidebarMenu

class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['sidebar_menu'] = SidebarMenu()
        return context
