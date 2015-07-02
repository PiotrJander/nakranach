from django import forms

from .models import ProfilePub


class InviteUserForm(forms.Form):
    email = forms.EmailField()
    role = forms.ChoiceField(choices=ProfilePub.ROLE_CHOICES)