from braces.views import UserFormKwargsMixin
from django.core.urlresolvers import reverse_lazy
from django.http.response import HttpResponseRedirect
from django.views.generic import FormView
from django_tables2 import SingleTableView

from app.users.forms import InviteUserForm
from app.users.models import Profile, ProfilePub
from app.users.tables import ManagedUsersTable


class AddPubToContextMixin(object):
    def get_pub(self):
        """Returns the pub managed by the logged-in user."""
        return self.request.profile.get_pub()

    def get_context_data(self, **kwargs):
        context = super(AddPubToContextMixin, self).get_context_data(**kwargs)
        context['pub'] = self.get_pub()
        return context


class ProfileListView(AddPubToContextMixin, SingleTableView):
    model = Profile
    table_class = ManagedUsersTable

    def get_table_data(self):
        """Queryset should only include users which are managed by the logged-in admin."""
        return self.request.profile.managed_users()

    def post(self, request, *args, **kwargs):
        """
        Assummes POST data has includes the action (remove|admin|employee|storeman) and points to a user U
        via profile_id. Also assumes the logged-in user manages pub P.
        If action is remove, removes user U from pub P.
        If action is one of admin|employee|storeman, changes user U's role in pub P to the role specified in the action.
        """
        profile_id = request.POST['profile_id']
        action = request.POST['action']
        if self.request.profile.id == profile_id:
            return HttpResponseRedirect(self.request.path)
            # we should complain here; admin can't change his role or remove himself from the pub
            # better yet disactivate buttons in the table
        if action == 'remove':
            ProfilePub.remove_from_pub(profile_id, self.get_pub())
        else:
            role = action  # we can assume action is admin|employee|storeman
            ProfilePub.change_role(profile_id, self.get_pub(), role)
        return HttpResponseRedirect(self.request.path)

    def get_table(self, **kwargs):
        kwargs['pub'] = self.get_pub()
        return super(ProfileListView, self).get_table(**kwargs)


class InviteUserView(UserFormKwargsMixin, FormView):
    template_name = 'users/invite.html'
    success_url = reverse_lazy('user:list')
    form_class = InviteUserForm

    def form_valid(self, form):
        """Creates a ProfilePub linking the user to the managed pub and containing her role."""

        # get profile
        user_email = form.cleaned_data['email']
        profile = Profile.get_by_email(user_email)

        # get role
        role = form.cleaned_data['role']

        # make and save relation
        pp = ProfilePub(pub=self.request.profile.get_pub(), profile=profile, role=role)
        pp.save()

        return super(InviteUserView, self).form_valid(form)
