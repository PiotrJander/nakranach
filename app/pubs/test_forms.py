from django.contrib.auth import get_user_model

from django.test import TestCase

from app.beers.models import Beer, Brewery, Style
from app.pubs.forms import ModifyWaitingBeerForm
from app.pubs.models import Pub, WaitingBeer
from app.users.models import Profile, ProfilePub


class TestModifyWaitingBeerForm(TestCase):
    def test_clean_beer_id(self):
        user = get_user_model().objects.create_user('a@a.com', 'pwd')
        profile = Profile.objects.create(user=user, name='Jan', surname='Nowak')
        pub = Pub.objects.create(name='Rademenes', city='Warszawa')
        ProfilePub.objects.create(profile=profile, pub=pub, role='storeman')
        beer = Beer.objects.create(name='Jasne', brewery=Brewery.objects.create(name='Matysiowo', country='Polska'),
                                   style=Style.objects.create(name='jasne'))
        waitingbeer = WaitingBeer.objects.create(pub=pub, beer=beer)
        waitingbeer_id = waitingbeer.id

        form_data = {'beer_id': waitingbeer_id, '_name': 'Matysiowo'}
        form = ModifyWaitingBeerForm(data=form_data, user=user)
        form.is_valid()
        form.save()
        waitingbeer.refresh_from_db()
        self.assertEquals(waitingbeer.name, 'Matysiowo')