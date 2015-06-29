from django.conf.urls import url

from .views import ProfileListView

urlpatterns = [
    url(r'^list/', view=ProfileListView.as_view(), name='list')
]