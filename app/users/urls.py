from django.conf.urls import url

from .views import ProfileListView, InviteUserView

urlpatterns = [
    url(r'^list/$', view=ProfileListView.as_view(), name='list'),
    url(r'^invite/$', view=InviteUserView.as_view(), name='invite')
]