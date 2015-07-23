from django.contrib.auth import get_user_model
from django import forms
from registration.forms import RegistrationFormUniqueEmail
from registration.users import UsernameField


class CustomUserRegistrationForm(RegistrationFormUniqueEmail):
    """Adjust the registration form to work with a user model without the username field."""
    first_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)

    class Meta:
        model = get_user_model()
        fields = (UsernameField(), 'first_name', 'last_name',)