from django import forms
from braces.forms import UserKwargModelFormMixin
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
    beer_id = forms.IntegerField()

    class Meta:
        model = WaitingBeer
        fields = ['beer_id', '_brewery', '_style', '_name', '_ibu', '_abv']

    def __init__(self, *args, **kwargs):
        super(ModifyWaitingBeerForm, self).__init__(*args, **kwargs)
        self.pub = self.user.profile.get_pub()

    def clean_beer_id(self):
        """
        Checks that ``beer_id`` represents a beer in the ``waiting_beers`` list in the ``user``'s pub.
        """
        beer_id = self.cleaned_data['beer_id']
        if not self.pub.has_beer(beer_id):
            raise forms.ValidationError('W pubie nie ma piwa o id %(id)s', params={'id': beer_id})
        self.instance = WaitingBeer.objects.get(id=beer_id)
        return beer_id