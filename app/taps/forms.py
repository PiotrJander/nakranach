from django import forms
from braces.forms import UserKwargModelFormMixin
from app.taps.form_helpers import ChangeBeerOnTapFormHelper


class ChangeBeerOnTapForm(UserKwargModelFormMixin, forms.Form):
    new_beer = forms.ChoiceField(label='Wybierz nowe piwo')

    helper = ChangeBeerOnTapFormHelper()

    def __init__(self, *args, **kwargs):
        super(ChangeBeerOnTapForm, self).__init__(*args, **kwargs)
        self.fields['new_beer'].choices = ((beer.id, beer.description())
                                                for beer in self.user.profile.get_pub().waiting_beers.all())