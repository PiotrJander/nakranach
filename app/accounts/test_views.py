from django.contrib.auth import get_user_model

from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, RequestFactory

from app.accounts.views import ProfileRegistrationView


class TestProfileRegistrationView(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.factory = RequestFactory()

    def test_post(self):
        data = {
            'email': 'a@a.com',
            'name': 'Jan',
            'surname': 'Kowalski',
            'password1': 'pwd',
            'password2': 'pwd',
        }
        request = self.factory.post('/accounts/register/', data)
        response = ProfileRegistrationView.as_view(request)
        try:
            new_user = get_user_model().objects.get(email='a@a.com')
        except ObjectDoesNotExist:
            self.fail("User account a@a.com was not created.")
        new_profile = new_user.profile
        self.assertEquals(new_user.email, 'a@a.com')
        self.assertTrue(new_user.check_password('pwd'))
        self.assertEquals(new_profile.name, 'Jan')
        self.assertEquals(new_profile.surname, 'Kowalski')
