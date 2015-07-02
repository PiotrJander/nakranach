from django import forms

from .models import ProfilePub, Profile


def invite_user_form_factory(profile):
    """
    Suppose user U is an admin in pubs P and R, and he wants to invite users
    in users:invite view. invite_user_form_factory function takes U's Profile as
    the argument and returns a customized form, ie. with pub choices being P and R.
    """
    # first we need managed pubs and
    pub_choices = ((pub.id, pub.name) for pub in profile.managed_pubs())
    class InviteUserForm(forms.Form):
        email = forms.EmailField()
        role = forms.ChoiceField(choices=ProfilePub.ROLE_CHOICES)
        pub = forms.ChoiceField(choices=pub_choices)
    return InviteUserForm