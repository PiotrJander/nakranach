from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from django import forms
from braces.forms import UserKwargModelFormMixin
from app.beers.models import Beer
from app.pubs.models import WaitingBeer


# class EditWaitingBeerMixin(UserKwargModelFormMixin, forms.Form):
#     beer_id = forms.IntegerField()
#
#     def __init__(self, *args, **kwargs):
#         super(EditWaitingBeerMixin, self).__init__(*args, **kwargs)
#         self.pub = self.user.profile.get_pub()
#
#     def clean_beer_id(self):
#         """
#         Checks that ``beer_id`` represents a beer in the ``waiting_beers`` list in the ``user``'s pub.
#         """
#         beer_id = self.cleaned_data['beer_id']
#         if not self.pub.has_beer(beer_id):
#             raise forms.ValidationError('W pubie nie ma piwa o id %(id)s', params={'id': beer_id})
#         return beer_id


class RemoveBeerFromWaitingBeersForm(UserKwargModelFormMixin, forms.Form):
    beer_id = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(RemoveBeerFromWaitingBeersForm, self).__init__(*args, **kwargs)
        self.pub = self.user.profile.get_pub()

    def clean_beer_id(self):
        """
        Checks that ``beer_id`` represents a beer in the ``waiting_beers`` list in the ``user``'s pub.
        """
        beer_id = self.cleaned_data['beer_id']
        if not self.pub.has_beer(beer_id):
            raise forms.ValidationError('W pubie nie ma piwa o id %(id)s', params={'id': beer_id})
        return beer_id

    def save(self):
        beer_id = self.cleaned_data['beer_id']
        self.pub.remove_beer(beer_id)


class ModifyWaitingBeerForm(UserKwargModelFormMixin, forms.ModelForm):
    beer_id = forms.IntegerField(widget=forms.HiddenInput)

    class Meta:
        model = WaitingBeer
        fields = ['beer_id', '_brewery', '_style', '_name', '_ibu', '_abv']

    def __init__(self, *args, **kwargs):
        super(ModifyWaitingBeerForm, self).__init__(*args, **kwargs)
        self.pub = self.user.profile.get_pub()
        self.helper = FormHelper(self)
        self.helper.form_action = 'pub:modify_beer'
        self.helper.form_id = 'waitingBeerForm'
        self.helper.layout = Layout(
            Field('beer_id', css_id="beerId"),
            '_brewery',
            '_name',
            '_style',
            Div(
                Field('_ibu', wrapper_class='col-sm-6'),
                Field('_abv', wrapper_class='col-sm-6'),
                css_class='row'
            )
        )

    def clean_beer_id(self):
        """
        Checks that ``beer_id`` represents a beer in the ``waiting_beers`` list in the ``user``'s pub.
        """
        beer_id = self.cleaned_data['beer_id']
        if not self.pub.has_beer(beer_id):
            raise forms.ValidationError('W pubie nie ma piwa o id %(id)s', params={'id': beer_id})
        self.instance = WaitingBeer.objects.get(id=beer_id)
        return beer_id


class DatabaseBeerDisabledForm(forms.ModelForm):

    class Meta:
        model = Beer
        fields = ['brewery', 'style', 'name', 'ibu', 'abv']
        widgets = {
            'brewery': forms.TextInput(),
            'style': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        super(DatabaseBeerDisabledForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'beerForm'
        self.helper.layout = Layout(
            Field('brewery', type='text', readonly=True),
            Field('name', readonly=True, ),
            Field('style', readonly=True),
            Div(
                Field('ibu', readonly=True, wrapper_class='col-sm-6'),
                Field('abv', readonly=True, wrapper_class='col-sm-6'),
                css_class='row'
            )
        )
