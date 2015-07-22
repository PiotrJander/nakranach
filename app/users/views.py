from django.views.generic import ListView, FormView
# from registration.backends.simple.views import RegistrationView
from registration.backends.simple.views import RegistrationView

from app.pubs.models import Pub
# from app.users.forms import CustomUserRegistrationForm
from .forms import CustomUserRegistrationForm
from .models import Profile, ProfilePub
from .forms import invite_user_form_factory


class ProfileRegistrationView(RegistrationView):
    """
    Works like RegistrationFormUniqueEmail, but on saving the user also creates a Profile and links that profile
    to the newly created user. Also handles first name and last name fields.
    """
    form_class = CustomUserRegistrationForm
    success_url = 'main:dashboard'

    def register(self, request, form):
        new_user = super(ProfileRegistrationView, self).register(request, form)
        Profile.objects.create(user=new_user, name=form.cleaned_data['first_name'], surname=form.cleaned_data['last_name'])
        return new_user


class ProfileListView(ListView):
    model = Profile

    def get_queryset(self):
        """Queryset should only include users which are managed by the logged-in admin."""
        profile = Profile.get_by_user(self.request.user)
        return profile.managed_users()
        # profile = Profile.get_by_user(self.request.user)
        # self.queryset = profile.managed_users()
        # return super(ProfileListView, self).get_queryset()


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


# class CustomUserRegistrationView(RegistrationView):
#     form_class = CustomUserRegistrationForm