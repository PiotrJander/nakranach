from django.views.generic import ListView


from .models import Profile

class ProfileListView(ListView):
    model = Profile

    def get_queryset(self):
        profile = Profile.get_by_user(self.request.user)
        self.queryset = profile.managed_users()
        return super(ProfileListView, self).get_queryset()
