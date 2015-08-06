from django.conf.urls import url
from app.users.views import ChangeRoleView, RemoveFromPubView

from .views import ProfileListView, InviteUserView

urlpatterns = [
    url(r'^list/$', view=ProfileListView.as_view(), name='list'),
    url(r'^invite/$', view=InviteUserView.as_view(), name='invite'),
    url(r'^change_role/$', view=ChangeRoleView.as_view(), name='change_role'),
    url(r'^remove/$', view=RemoveFromPubView.as_view(), name='remove'),
]