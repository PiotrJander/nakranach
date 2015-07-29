# coding=utf-8
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationFormUniqueEmail
from registration.users import UsernameField
from app.accounts.form_helpers import profile_update_form_helper
from app.users.models import Profile


class CustomUserRegistrationForm(RegistrationFormUniqueEmail):
    """Adjust the registration form to work with a user model without the username field."""
    first_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)

    class Meta:
        model = get_user_model()
        fields = (UsernameField(), 'first_name', 'last_name',)


class AuthenticationFormWithRememberMe(AuthenticationForm):
    """Extends the default authentication form with a 'remember me' field."""
    remember_me = forms.BooleanField(label=_(u'zapamiętaj mnie'), required=False)


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    helper = profile_update_form_helper

    def save(self, commit=True):
        """Saves the email additionally."""
        profile = super(ProfileUpdateForm, self).save()
        profile.user.email = self.cleaned_data['email']
        profile.user.save()

    class Meta:
        model = Profile
        fields = ['email', 'name', 'surname']
