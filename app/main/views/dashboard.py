from django.views.generic import TemplateView

from braces.views import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'main/dashboard.html'

