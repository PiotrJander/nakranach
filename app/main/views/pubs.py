from django.views.generic import TemplateView, DetailView

from app.pubs.models import Pub

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        return context

class PubView(DetailView):
    template_name = 'pub.html'
    model = Pub