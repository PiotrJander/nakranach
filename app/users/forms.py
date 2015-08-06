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


class ManageUserForm(UserKwargModelFormMixin, forms.Form):
    user_id = forms.IntegerField()

    def clean_user_id(self):
        """
        Checks that the user identified by the id can be managed by the logged in user.
        """
        user_id = self.cleaned_data['user_id']
        if not self.user.profile.managed_users(id=user_id):
            raise forms.ValidationError(_('Nie masz uprawnień, żeby zmienić rolę tego użytkownika'))
        return user_id

    def get_user_to_modify(self):
        return Profile.objects.get(id=self.cleaned_data['user_id'])


class ChangeRoleForm(ManageUserForm):
    role = forms.ChoiceField(choices=ProfilePub.ROLE_CHOICES)

    def save(self):
        user = self.get_user_to_modify()
        user.profilepub_set.update(role=self.clenead_data['role'])


class RemoveFromPubForm(ManageUserForm):
    def save(self):
        user = self.get_user_to_modify()
        user.profilepub_set.all().delete()