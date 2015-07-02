from django.views.generic import ListView, FormView

from .models import Profile
from .forms import InviteUserForm

class ProfileListView(ListView):
    model = Profile

    def get_queryset(self):
        profile = Profile.get_by_user(self.request.user)
        self.queryset = profile.managed_users()
        return super(ProfileListView, self).get_queryset()


class InviteUserView(FormView):
    form_class = InviteUserForm
    template_name = 'users/invite.html'
    success_url = '/user/list'