from django.views.generic import ListView


from .models import Profile

class ProfileListView(ListView):
    model = Profile
    # context_object_name = 'users'

    def get_queryset(self):
        profile = Profile.get_by_user(self.request.user)
        self.queryset = profile.managed_users()
        return super(ProfileListView, self).get_queryset()

    def get_paginate_orphans(self):
        return super(ProfileListView, self).get_paginate_orphans()

