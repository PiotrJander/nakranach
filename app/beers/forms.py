# coding=utf-8
from crispy_forms.helper import FormHelper
from crispy_forms import layout
from django import forms
from django.forms.models import fields_for_model

from app.beers.models import Beer, Brewery


class CreateBeerForm(forms.ModelForm):
    """
    The form has fields: name, brewery, style, ibu, abv, create_new_brewery, brewery_name, brewery_country.

    An existing brewery is associated with the new beer if ``create_new_brewery`` is not selected. Otherwise a new
    brewery is created. So the following logic is implemented in the ``clean`` method:

    * If ``create_new_brewery`` is not selected, then ``brewery`` ModelChoiceField is required.
    * Else ``brewery_name`` and ``brewery_country`` fields are required.
    """
    class Meta:
        model = Beer
        fields = ['name', 'brewery', 'style', 'ibu', 'abv']

    create_new_brewery = forms.BooleanField(label=u'Utwórz nowy browar', required=False)

    # the form has two more fields, but they need to be added dynamically in __init__
    # brewery_name
    # brewery_country

    def __init__(self, *args, **kwargs):
        super(CreateBeerForm, self).__init__(*args, **kwargs)

        # add fields from the Brewery model
        brewery_fields = fields_for_model(Brewery, fields=['name', 'country'])
        self.fields['brewery_name'] = brewery_fields['name']
        self.fields['brewery_name'].required = False
        self.fields['brewery_name'].label = 'Nazwa browaru'
        self.fields['brewery_country'] = brewery_fields['country']
        self.fields['brewery_country'].required = False
        self.fields['brewery_country'].label = 'Kraj browaru'

        # Brewery ModelChoiceField should not be required 
        self.fields['brewery'].required = False

        # crispy form helper
        self.helper = FormHelper()
        self.helper.form_action = 'beer:create'
        self.helper.form_id = 'createBeerForm'
        self.helper.html5_required = True
        self.helper.layout = layout.Layout(
            layout.Field('brewery', id='chooseBreweryField'),
            layout.Div(
                layout.Field('brewery_name', wrapper_class='col-sm-6'),
                layout.Field('brewery_country', wrapper_class='col-sm-6'),
                css_class='row',
                css_id='addNewBreweryInputs'
            ),
            layout.Field('create_new_brewery', id='createNewBreweryCheckbox'),
            'name',
            layout.Field('style', id='chooseStyleField'),
            layout.Div(
                layout.Field('ibu', wrapper_class='col-sm-6'),
                layout.Field('abv', wrapper_class='col-sm-6'),
                css_class='row',
            ),
        )

    def clean(self):
        if self.cleaned_data['create_new_brewery']:
            brewery_name = self.check_brewery_name_is_not_blank()
            brewery_country = self.check_brewery_country_is_not_blank()
            if brewery_name and brewery_country:
                new_brewery = Brewery.objects.create(name=brewery_name, country=brewery_country)
                self.cleaned_data['brewery'] = new_brewery
        else:
            self.check_brewery_is_not_blank()

    def check_brewery_is_not_blank(self):
        if not self.cleaned_data['brewery']:
            self.add_error('brewery', u'Nie wybrałeś opcji tworzenia nowego browaru. Musisz wybrać istniejący browar'
                                      'z listy')

    def check_brewery_name_is_not_blank(self):
        brewery_name = self.cleaned_data['brewery_name']
        if brewery_name:
            return brewery_name
        else:
            self.add_error('brewery_name', u'Wybrałeś opcję tworzenia nowego browaru. '
                                           u'Musisz podać nazwę browaru.')

    def check_brewery_country_is_not_blank(self):
        brewery_country = self.cleaned_data['brewery_country']
        if brewery_country:
            return brewery_country
        else:
            self.add_error('brewery_country', u'Wybrałeś opcję tworzenia nowego browaru. '
                                              u'Musisz podać kraj browaru.')
