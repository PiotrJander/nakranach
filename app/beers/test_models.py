from django.db.models.query import QuerySet
from django.test import TestCase
from app.beers.models import Beer, Brewery, Style


class TestBeer(TestCase):
    def test_export_form_data(self):
        beer = Beer.objects.create(name='Jasne', brewery=Brewery.objects.create(name='Matysiowo', country='Polska'),
                                   style=Style.objects.create(name='jasne'), ibu=18, abv=0.5)
        dictionary = beer.export_form_data()
        expected_dict = {'abv': u'0.5', 'style': u'jasne', 'brewery': u'Matysiowo', 'ibu': u'18', 'name': u'Jasne'}
        self.assertDictEqual(dictionary, expected_dict)

    def test_match(self):
        """
        Check that, given the argument ``search_string``, the ``match`` classmethod returns only those ``Beer``s
        whose ``search`` field contains the ``search_string``.
        """
        style = Style.objects.create(name='Bock')
        beer1 = Beer.objects.create(name='Tysiowe', brewery=Brewery.objects.create(name='Matysiowo', country='Polska'),
                                    style=style)
        beer2 = Beer.objects.create(name='Zagloba', brewery=Brewery.objects.create(name='Ziemianski', country='Polska'),
                                    style=style)
        got = Beer.match('Ziemianski  Zagloba')
        expected = Beer.objects.filter(pk=beer2.pk)
        self.assertQuerysetEqual(got, expected)