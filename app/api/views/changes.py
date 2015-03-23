from app.pubs import models as pubs_models
from app.taps import models as taps_models

from rest_framework.generics import GenericAPIView

from .helpers import tap_changes_response
from .mixins import AuthMixin
from app.api.pagination import TapChangePagination

class ChangesView(AuthMixin, GenericAPIView):
    # http://www.django-rest-framework.org/api-guide/permissions/#djangomodelpermissions
    queryset = taps_models.TapChange.objects.all()
    pagination_class = TapChangePagination

    def get(self, request, format=None):
        return tap_changes_response(self.queryset, request, self)