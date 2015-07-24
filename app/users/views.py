from django.views.generic import ListView, FormView

from app.pubs.models import Pub
from .models import Profile, ProfilePub
from .forms import invite_user_form_factory


class ProfileListView(ListView):
    # TODO secure the form
    model = Profile

    def get_queryset(self):
        """Queryset should only include users which are managed by the logged-in admin."""
        profile = Profile.get_by_user(self.request.user)
        return profile.managed_users()

    def post(self, request, *args, **kwargs):
        pass


class InviteUserView(FormView):
    template_name = 'users/invite.html'
    success_url = '/user/list'

    def get_form_class(self):
        profile = Profile.get_by_user(self.request.user)
        return invite_user_form_factory(profile)

    def form_valid(self, form):
        # get pub
        pub_id = form.cleaned_data['pub']
        pub = Pub.get_by_id(pub_id)

        # get profile
        user_email = form.cleaned_data['email']
        profile = Profile.get_by_email(user_email)

        # get role
        role = form.cleaned_data['role']

        # make and save relation
        pp = ProfilePub(pub=pub, profile=profile, role=role)
        pp.save()

        return super(InviteUserView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        "Add user profile to the context."
        context = super(InviteUserView, self).get_context_data(**kwargs)
        context['profile'] = Profile.get_by_user(self.request.user)
        return context
