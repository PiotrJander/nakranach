from django.test import TestCase
from app.beers.models import Beer, Brewery, Style


class TestBeer(TestCase):
    def test_export_form_data(self):
        beer = Beer.objects.create(name='Jasne', brewery=Brewery.objects.create(name='Matysiowo', country='Polska'),
                                   style=Style.objects.create(name='jasne'), ibu=18, abv=0.5)
        dictionary = beer.export_form_data()
        expected_dict = {'abv': u'0.5', 'style': u'jasne', 'brewery': u'Matysiowo', 'ibu': u'18', 'name': u'Jasne'}
        self.assertDictEqual(dictionary, expected_dict)