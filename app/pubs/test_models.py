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
        WaitingBeer.objects.create(pub=pub, beer=beer)

        # first implication
        beer_id = beer.id
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
        WaitingBeer.objects.create(pub=pub, beer=beer)

        # try to delete a beer which is in the pub
        beer_id = beer.id
        pub.remove_beer(beer_id)
        self.assertFalse(pub.has_beer(beer_id))