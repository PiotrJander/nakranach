from django.contrib.auth import get_user_model
from django.test import TestCase
from app.beers.forms import CreateBeerForm
from app.beers.models import Style, Brewery, Beer
from app.pubs.models import Pub
from app.users.models import Profile, ProfilePub


class TestCreateBeerForm(TestCase):
    def test_the_form_can_be_instantiated(self):
        user = get_user_model().objects.create_user('a@a.com', 'pwd')
        profile = Profile.objects.create(user=user, name='Jan', surname='Nowak')
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        ProfilePub.objects.create(profile=profile, pub=pub, role='storeman')
        CreateBeerForm(user=user)

    def test_form_valid_with_create_new_brewery_and_valid_data(self):
        user = get_user_model().objects.create_user('a@a.com', 'pwd')
        profile = Profile.objects.create(user=user, name='Jan', surname='Nowak')
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        ProfilePub.objects.create(profile=profile, pub=pub, role='storeman')
        style = Style.objects.create(name='ale')
        brewery = Brewery.objects.create(name='Matysiowo', country='Poland')

        data = {
            'name': 'Matysiowe',
            'brewery': '',
            'style': style.id,
            'ibu': '',
            'abv': '',
            'create_new_brewery': 'on',
            'brewery_name': 'Tyskie',
            'brewery_country': 'Poland',
        }

        form = CreateBeerForm(data=data, user=user)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_create_new_brewery_and_blank_brewery_name(self):
        user = get_user_model().objects.create_user('a@a.com', 'pwd')
        profile = Profile.objects.create(user=user, name='Jan', surname='Nowak')
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        ProfilePub.objects.create(profile=profile, pub=pub, role='storeman')
        style = Style.objects.create(name='ale')
        brewery = Brewery.objects.create(name='Matysiowo', country='Poland')

        data = {
            'name': 'Matysiowe',
            'brewery': '',
            'style': style.id,
            'ibu': '',
            'abv': '',
            'create_new_brewery': 'on',
            'brewery_name': '',
            'brewery_country': 'Poland',
        }

        form = CreateBeerForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    def test_form_invalid_with_create_new_brewery_and_blank_brewery_country(self):
        user = get_user_model().objects.create_user('a@a.com', 'pwd')
        profile = Profile.objects.create(user=user, name='Jan', surname='Nowak')
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        ProfilePub.objects.create(profile=profile, pub=pub, role='storeman')
        style = Style.objects.create(name='ale')
        brewery = Brewery.objects.create(name='Matysiowo', country='Poland')

        data = {
            'name': 'Matysiowe',
            'brewery': '',
            'style': style.id,
            'ibu': '',
            'abv': '',
            'create_new_brewery': 'on',
            'brewery_name': 'Tyskie',
            'brewery_country': '',
        }

        form = CreateBeerForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    def test_valid_form_with_create_new_brewery_saves(self):
        user = get_user_model().objects.create_user('a@a.com', 'pwd')
        profile = Profile.objects.create(user=user, name='Jan', surname='Nowak')
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        ProfilePub.objects.create(profile=profile, pub=pub, role='storeman')
        style = Style.objects.create(name='ale')
        brewery = Brewery.objects.create(name='Matysiowo', country='Poland')

        data = {
            'name': 'Matysiowe',
            'brewery': '',
            'style': style.id,
            'ibu': '',
            'abv': '',
            'create_new_brewery': 'on',
            'brewery_name': 'Tyskie',
            'brewery_country': 'Poland',
        }

        form = CreateBeerForm(data=data, user=user)
        beer = form.save()

        self.assertTrue(Beer.objects.filter(name='Matysiowe'))
        self.assertTrue(form.pub.has_beer(beer.id))

    def test_form_valid_with_not_create_new_brewery_and_valid_data(self):
        user = get_user_model().objects.create_user('a@a.com', 'pwd')
        profile = Profile.objects.create(user=user, name='Jan', surname='Nowak')
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        ProfilePub.objects.create(profile=profile, pub=pub, role='storeman')
        style = Style.objects.create(name='ale')
        brewery = Brewery.objects.create(name='Matysiowo', country='Poland')

        data = {
            'name': 'Matysiowe',
            'brewery': brewery.id,
            'style': style.id,
            'ibu': '',
            'abv': '',
            # 'create_new_brewery': '',
            'brewery_name': '',
            'brewery_country': '',
        }

        form = CreateBeerForm(data=data, user=user)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_not_create_new_brewery_and_blank_brewery(self):
        user = get_user_model().objects.create_user('a@a.com', 'pwd')
        profile = Profile.objects.create(user=user, name='Jan', surname='Nowak')
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        ProfilePub.objects.create(profile=profile, pub=pub, role='storeman')
        style = Style.objects.create(name='ale')
        brewery = Brewery.objects.create(name='Matysiowo', country='Poland')

        data = {
            'name': 'Matysiowe',
            'brewery': '',
            'style': style.id,
            'ibu': '',
            'abv': '',
            'create_new_brewery': '',
            'brewery_name': '',
            'brewery_country': '',
        }

        form = CreateBeerForm(data=data, user=user)
        self.assertFalse(form.is_valid())

    def test_valid_form_with_not_create_new_brewery_saves(self):
        user = get_user_model().objects.create_user('a@a.com', 'pwd')
        profile = Profile.objects.create(user=user, name='Jan', surname='Nowak')
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        ProfilePub.objects.create(profile=profile, pub=pub, role='storeman')
        style = Style.objects.create(name='ale')
        brewery = Brewery.objects.create(name='Matysiowo', country='Poland')

        data = {
            'name': 'Matysiowe',
            'brewery': brewery.id,
            'style': style.id,
            'ibu': '',
            'abv': '',
            'create_new_brewery': '',
            'brewery_name': '',
            'brewery_country': '',
        }

        form = CreateBeerForm(data=data, user=user)
        beer = form.save()

        self.assertTrue(Beer.objects.filter(name='Matysiowe'))
        self.assertTrue(form.pub.has_beer(beer.id))
