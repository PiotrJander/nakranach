from braces.views import UserFormKwargsMixin
from django.contrib.auth import views as auth_views, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http.response import HttpResponseRedirect
from django.views.generic.edit import FormView
from registration.backends.simple.views import RegistrationView

from app.accounts.forms import CustomUserRegistrationForm, AuthenticationFormWithRememberMe, ProfileUpdateForm
from app.accounts.form_helpers import RegisterFormHelper, PasswordChangeFormHelper
from app.users.models import Profile


class ProfileRegistrationView(RegistrationView):
    """
    Works like RegistrationFormUniqueEmail, but on saving the user also creates a Profile and links that profile
    to the newly created user. Also handles first name and last name fields.
    """
    form_class = CustomUserRegistrationForm
    success_url = 'main:dashboard'

    def register(self, request, form):
        new_user = super(ProfileRegistrationView, self).register(request, form)
        Profile.objects.create(user=new_user, name=form.cleaned_data['name'],
                               surname=form.cleaned_data['surname'])
        return new_user

    def get_context_data(self, **kwargs):
        context = super(ProfileRegistrationView, self).get_context_data(**kwargs)
        context['form_helper'] = RegisterFormHelper()
        return context


class ProfileUpdateView(UserFormKwargsMixin, FormView):
    template_name = 'registration/profile_update.html'
    form_class = ProfileUpdateForm

    def get_initial(self):
        return {'email': self.request.user.email}

    def get_form_kwargs(self):
        kwargs = super(ProfileUpdateView, self).get_form_kwargs()
        kwargs['instance'] = self.request.profile
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context.update({
            'password_change_form': PasswordChangeForm(user=self.request.user),
            'password_change_form_helper': PasswordChangeFormHelper()
        })
        return context

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.request.path)


#  login view

def login_with_remember_me(request, *args, **kwargs):
    """Sets the session to expire when the user closes the browser unless the user checks 'remember me'."""
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)

    # use custom form
    kwargs['authentication_form'] = AuthenticationFormWithRememberMe
    return auth_views.login(request, *args, **kwargs)