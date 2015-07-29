from django.contrib.auth import views as auth_views, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from registration.backends.simple.views import RegistrationView
from app.accounts.forms import CustomUserRegistrationForm, AuthenticationFormWithRememberMe, ProfileUpdateForm
from app.accounts.form_helpers import register_form_helper, password_change_form_helper
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
        context['form_helper'] = register_form_helper
        return context


class ProfileUpdateView(FormView):
    form_class = ProfileUpdateForm
    success_url = '/accounts/profile/update/'
    template_name = 'registration/profile_update.html'

    def form_valid(self, form):
        """Additionally save form data."""
        form.save()
        return super(ProfileUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        context.update({
            'profile': Profile.get_by_user(self.request.user),
            'password_change_form_helper': password_change_form_helper,
        })
        if 'password_change_form' not in context:
            context['password_change_form'] = PasswordChangeForm(user=self.request.user)
        return context

    def get_form_kwargs(self):
        """Pass the 'instance' kwarg to the form."""
        kwargs = super(ProfileUpdateView, self).get_form_kwargs()
        # kwargs['instance'] = Profile.get_by_user(self.request.user)
        kwargs.update({
            'instance': Profile.get_by_user(self.request.user),
            'initial': {'email': self.request.user.email},
        })
        return kwargs

    def post(self, request, *args, **kwargs):
        if 'password_change' in request.POST:
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                # Updating the password logs out all other sessions for the user
                # except the current one if
                # django.contrib.auth.middleware.SessionAuthenticationMiddleware
                # is enabled.
                update_session_auth_hash(request, form.user)
                return self.get(request)
            else:
                password_change_form = form
                form = self.get_form()
                return self.render_to_response(self.get_context_data(password_change_form=password_change_form, form=form))
        else:
            return super(ProfileUpdateView, self).post(request)


# class ProfileUpdateView(TemplateView):
#     template_name = 'registration/profile_update.html'
#
#     def get(self, request, *args, **kwargs):
#         # prepare forms
#         profile_update_form = ProfileUpdateForm(instance=self.request.profile,
#                                                 initial={'email': self.request.user.email})
#         password_change_form = PasswordChangeForm(user=self.request.user)
#         password_change_form.helper = password_change_form_helper
#         # update context
#         context = self.get_context_data(profile_update_form=profile_update_form,
#                                         password_change_form=password_change_form)
#         # render
#         return self.render_to_response(context)
#
#     def post(self, request, *args, **kwargs):
#         pass


#  login view

def login_with_remember_me(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)

    # use custom form
    kwargs['authentication_form'] = AuthenticationFormWithRememberMe
    return auth_views.login(request, *args, **kwargs)