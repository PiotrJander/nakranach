from app.pubs import models as pubs_models
from app.taps import models as taps_models

from rest_framework.views import APIView

from .helpers import tap_changes_response
from .mixins import AuthMixin

class ChangesView(AuthMixin, APIView):
    # http://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions
    queryset = taps_models.TapChange.objects.all()

    def get(self, request, format=None):
        return tap_changes_response(self.queryset, request, 10)