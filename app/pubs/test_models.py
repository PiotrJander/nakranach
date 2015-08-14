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