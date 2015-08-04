from braces.views import UserFormKwargsMixin
from django.contrib.auth import views as auth_views, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http.response import HttpResponseRedirect
from registration.backends.simple.views import RegistrationView
from app.accounts.forms import CustomUserRegistrationForm, AuthenticationFormWithRememberMe, ProfileUpdateForm
from app.accounts.form_helpers import RegisterFormHelper, PasswordChangeFormHelper
from app.main.forms import MultiFormsView
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
        Profile.objects.create(user=new_user, name=form.cleaned_data['first_name'],
                               surname=form.cleaned_data['last_name'])
        return new_user

    def get_context_data(self, **kwargs):
        context = super(ProfileRegistrationView, self).get_context_data(**kwargs)
        context['form_helper'] = RegisterFormHelper()
        return context


class ProfileUpdateView(MultiFormsView):
    template_name = 'registration/profile_update.html'
    form_classes = {'email_name': ProfileUpdateForm,
                    'password_change': PasswordChangeForm, }

    def get_email_name_initial(self):
        return {'email': self.request.user.email}

    def create_email_name_form(self, **kwargs):
        kwargs['instance'] = self.request.profile
        kwargs['user'] = self.request.user
        return ProfileUpdateForm(**kwargs)

    def create_password_change_form(self, **kwargs):
        kwargs['user'] = self.request.user
        form = PasswordChangeForm(**kwargs)
        form.helper = PasswordChangeFormHelper()
        return form

    def email_name_form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.request.path)

    def password_change_form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one if
        # django.contrib.auth.middleware.SessionAuthenticationMiddleware
        # is enabled.
        update_session_auth_hash(self.request, form.user)
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