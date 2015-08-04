# coding=utf-8
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms
from braces.forms import UserKwargModelFormMixin
from .models import ProfilePub, Profile


class InviteUserForm(UserKwargModelFormMixin, forms.Form):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=ProfilePub.ROLE_CHOICES)

    def __init__(self, *args, **kwargs):
        super(InviteUserForm, self).__init__(*args, **kwargs)
        self.pub = self.user.profile.get_pub()

    def clean_email(self):
        """
        Checks if the email is already registered.
        Also ensures the email has not been associated with the pub yet.
        Adds a ValidationError to email field otherwise.
        """
        email = self.cleaned_data['email']
        if not Profile.check_email_is_registered(email):
            raise ValidationError(
                _(email_not_registered_error_msg),
                params={'email': email},
            )

        profile = Profile.get_by_email(email)
        if ProfilePub.objects.filter(profile=profile, pub=self.pub):
            # profile and pub are already associated
            self.add_error('email', ValidationError(
                _(email_already_associated_error_msg),
                params={'email': email}
            ))

        return email


# error messages

email_not_registered_error_msg = u"""
Wprowadzony adres email %(email)s nie jest zarejestrowany w Nakranach.
Upewnij się, że użytkownik, którego chcesz zaprosić, jest zarejestrowany.
Upewnij się też, że wprowadzony adres email jest poprawny.
"""

email_already_associated_error_msg = u"""
Użytkownik o adresie email %(email)s pełni już rolę w pubie.
Jeżeli chcesz zmienić rolę lub usunąć użytkownika z pubu, zrób to w widoku
listy użytkowników.
"""