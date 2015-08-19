from django.test import TestCase
from app.beers.models import Beer, Brewery, Style
from app.pubs.models import Pub, WaitingBeer


class TestPub(TestCase):
    def test_has_beer(self):
        """
        For pub P and beer B with id ID, P.has_beer(ID) should return True iff P has B.
        """
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        beer = Beer.objects.create(name='Jasne', brewery=Brewery.objects.create(name='Matysiowo', country='Polska'),
                                   style=Style.objects.create(name='jasne'))
        waitingbeer = WaitingBeer.objects.create(pub=pub, beer=beer)

        # first implication
        beer_id = waitingbeer.id
        self.assertTrue(pub.has_beer(beer_id))

        # second implication
        nonexistent_beer_id = beer_id + 10
        self.assertFalse(pub.has_beer(nonexistent_beer_id))

    def test_remove_beer(self):
        """
        Given that pub P has beer B with id ID, when P.remove_beer(ID) is called, then this should result in removing
        beer B from the pub.
        """
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        beer = Beer.objects.create(name='Jasne', brewery=Brewery.objects.create(name='Matysiowo', country='Polska'),
                                   style=Style.objects.create(name='jasne'))
        waitingbeer = WaitingBeer.objects.create(pub=pub, beer=beer)

        # try to delete a beer which is in the pub
        beer_id = waitingbeer.id
        pub.remove_beer(beer_id)
        self.assertFalse(pub.has_beer(beer_id))

    def test_add_waiting_beer(self):
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        beer = Beer.objects.create(name='Jasne', brewery=Brewery.objects.create(name='Matysiowo', country='Polska'),
                                   style=Style.objects.create(name='jasne'))
        pub.add_waiting_beer(beer.id)
        self.assertTrue(pub.waiting_beers.filter(id=beer.id).exists())


class TestWaitingBeer(TestCase):
    def test_waiting_beer_uses_beer_fields_by_default(self):
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        beer = Beer.objects.create(name='Jasne', brewery=Brewery.objects.create(name='Matysiowo', country='Polska'),
                                   style=Style.objects.create(name='jasne'))
        waitingbeer = WaitingBeer.objects.create(pub=pub, beer=beer)

        # assert that if the waiting beer doesn't override any field, than it uses beer fields
        beer_fields = (beer.name, beer.brewery, beer.style, beer.ibu, beer.abv)
        waitingbeer_values = (waitingbeer.name, waitingbeer.brewery, waitingbeer.style, waitingbeer.ibu, waitingbeer.abv)
        self.assertTupleEqual(beer_fields, waitingbeer_values)

        # assert that the waiting beer can override a beer field
        waitingbeer._name = 'Ciemne'
        self.assertEquals(waitingbeer.name, 'Ciemne')

    def test_export_form_data(self):
        """
        Should return a dict with ['brewery', 'style', 'name', 'ibu', 'abv'] attrs of the instance.
        """
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        beer = Beer.objects.create(name='Jasne', brewery=Brewery.objects.create(name='Matysiowo', country='Polska'),
                                   style=Style.objects.create(name='jasne'))
        waitingbeer = WaitingBeer.objects.create(pub=pub, beer=beer)
        waitingbeer._name = 'Jasne (promocja!)'
        dictionary = waitingbeer.export_form_data()
        expected_dict = {'_ibu': None, '_abv': None, '_name': 'Jasne (promocja!)', '_style': u'', '_brewery': u''}
        self.assertDictEqual(dictionary, expected_dict)

    def test_export_form_data_with_beer(self):
        """
        Should return a dict with ['brewery', 'style', 'name', 'ibu', 'abv'] attrs of the instance.
        """
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        beer = Beer.objects.create(name='Jasne', brewery=Brewery.objects.create(name='Matysiowo', country='Polska'),
                                   style=Style.objects.create(name='jasne'))
        waitingbeer = WaitingBeer.objects.create(pub=pub, beer=beer)
        waitingbeer._name = 'Jasne (promocja!)'
        dictionary = waitingbeer.export_form_data_with_beer()
        expected_dict = {
            'waitingbeer': {'_ibu': None, '_abv': None, '_name': 'Jasne (promocja!)', '_style': u'', '_brewery': u''},
            'beer': {'abv': u'None', 'style': u'jasne', 'brewery': u'Matysiowo', 'ibu': u'None', 'name': u'Jasne'},
        }
        self.assertDictEqual(dictionary, expected_dict)