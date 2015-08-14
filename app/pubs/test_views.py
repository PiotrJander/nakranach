from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import RequestFactory
from app.beers.models import Beer, Brewery, Style
from app.pubs.models import Pub, WaitingBeer
from app.pubs.views import RemoveBeerFromWaitingBeersView, ModifyWaitingBeerView
from app.users.models import Profile, ProfilePub


class TestRemoveBeerFromWaitingBeersView(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestRemoveBeerFromWaitingBeersView, cls).setUpClass()
        cls.factory = RequestFactory()

    def test_form_valid(self):
        user = get_user_model().objects.create_user('a@a.com', 'pwd')
        profile = Profile.objects.create(user=user, name='Jan', surname='Nowak')
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        ProfilePub.objects.create(profile=profile, pub=pub, role='storeman')
        beer = Beer.objects.create(name='Jasne', brewery=Brewery.objects.create(name='Matysiowo', country='Polska'),
                                   style=Style.objects.create(name='jasne'))
        waitingbeer = WaitingBeer.objects.create(pub=pub, beer=beer)
        beer_id = waitingbeer.id
        request = self.factory.post('', {'beer_id': beer_id})
        request.user = user
        response = RemoveBeerFromWaitingBeersView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(pub.has_beer(beer_id))

    def test_form_invalid(self):
        user = get_user_model().objects.create_user('a@a.com', 'pwd')
        profile = Profile.objects.create(user=user, name='Jan', surname='Nowak')
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        ProfilePub.objects.create(profile=profile, pub=pub, role='storeman')
        beer = Beer.objects.create(name='Jasne', brewery=Brewery.objects.create(name='Matysiowo', country='Polska'),
                                   style=Style.objects.create(name='jasne'))
        waitingbeer = WaitingBeer.objects.create(pub=pub, beer=beer)
        nonexistent_beer_id = waitingbeer.id + 10
        request = self.factory.post('', {'beer_id': nonexistent_beer_id})
        request.user = user
        response = RemoveBeerFromWaitingBeersView.as_view()(request)
        self.assertEqual(response.status_code, 400)


class TestModifyWaitingBeerView(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestModifyWaitingBeerView, cls).setUpClass()
        cls.factory = RequestFactory()

    def test_form_valid(self):
        user = get_user_model().objects.create_user('a@a.com', 'pwd')
        profile = Profile.objects.create(user=user, name='Jan', surname='Nowak')
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        ProfilePub.objects.create(profile=profile, pub=pub, role='storeman')
        beer = Beer.objects.create(name='Jasne', brewery=Brewery.objects.create(name='Matysiowo', country='Polska'),
                                   style=Style.objects.create(name='jasne'))
        waitingbeer = WaitingBeer.objects.create(pub=pub, beer=beer)
        beer_id = waitingbeer.id
        request = self.factory.post('', {'beer_id': beer_id, '_name': 'OldAle',})
        request.user = user
        response = ModifyWaitingBeerView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        waitingbeer.refresh_from_db()
        self.assertEqual(waitingbeer.name, 'OldAle')

    def test_form_invalid(self):
        user = get_user_model().objects.create_user('a@a.com', 'pwd')
        profile = Profile.objects.create(user=user, name='Jan', surname='Nowak')
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        ProfilePub.objects.create(profile=profile, pub=pub, role='storeman')
        beer = Beer.objects.create(name='Jasne', brewery=Brewery.objects.create(name='Matysiowo', country='Polska'),
                                   style=Style.objects.create(name='jasne'))
        waitingbeer = WaitingBeer.objects.create(pub=pub, beer=beer)
        nonexistent_beer_id = waitingbeer.id + 10
        request = self.factory.post('', {'beer_id': nonexistent_beer_id})
        request.user = user
        response = ModifyWaitingBeerView.as_view()(request)
        self.assertEqual(response.status_code, 400)
