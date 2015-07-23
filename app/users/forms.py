# coding=utf-8
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms


from app.pubs.models import Pub
from .models import ProfilePub, Profile


def invite_user_form_factory(profile):
    """
    Suppose user U is an admin in pubs P and R, and he wants to invite users
    in user:invite view. invite_user_form_factory function takes U's Profile as
    the argument and returns a customized form, ie. with pub choices being P and R.
    """
    # first we need managed pubs and
    pub_choices = ((pub.id, pub.name) for pub in profile.managed_pubs())

    class InviteUserForm(forms.Form):
        email = forms.EmailField()
        role = forms.ChoiceField(choices=ProfilePub.ROLE_CHOICES)
        pub = forms.ChoiceField(choices=pub_choices)

        def clean_email(self):
            """Checks if the email is already registered."""
            email = self.cleaned_data['email']
            if not Profile.check_email_is_registered(email):
                raise ValidationError(
                    _(email_not_registered_error_msg),
                    code='invalid',
                    params={'email': email},
                )
            return email

        def clean(self):
            """
            Ensures the email has not been associated with the pub yet.
            Adds a ValidationError to email field otherwise.
            """
            cleaned_data = super(InviteUserForm, self).clean()
            email = cleaned_data.get('email')
            pub_id = cleaned_data.get('pub')

            if not email:
                # email validation failed, cross field clean doesn't make sense
                return

            profile = Profile.get_by_email(email)
            pub = Pub.get_by_id(pub_id)
            if ProfilePub.objects.filter(profile=profile, pub=pub):
                # profile and pub are already associated
                self.add_error('email', email_already_associated_error_msg % {'email': email})

    return InviteUserForm


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
