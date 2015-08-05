from django import forms
from braces.forms import UserKwargModelFormMixin
from app.taps.form_helpers import ChangeBeerOnTapFormHelper


class ChangeBeerOnTapForm(UserKwargModelFormMixin, forms.Form):
    tap_id = forms.IntegerField(widget=forms.HiddenInput)
    waiting_beers = forms.ChoiceField(label='Wybierz nowe piwo')

    helper = ChangeBeerOnTapFormHelper()
    #
    def __init__(self, *args, **kwargs):
        super(ChangeBeerOnTapForm, self).__init__(*args, **kwargs)
        self.fields['waiting_beers'].choices = ((str(beer.id), beer.description())
                                                for beer in self.user.profile.get_pub().waiting_beers.all())
        # self.helper = ChangeBeerOnTapFormHelper()