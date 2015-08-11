from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, RequestFactory
from app.accounts.forms import CustomUserRegistrationForm

from app.accounts.views import ProfileRegistrationView
from app.main.utils import add_middleware_to_request, setup_view


class TestProfileRegistrationView(TestCase):
    form_data = {
        'email': 'a@a.com',
        'name': 'Jan',
        'surname': 'Kowalski',
        'password1': 'pwd',
        'password2': 'pwd',
    }

    @classmethod
    def setUpClass(cls):
        super(TestProfileRegistrationView, cls).setUpClass()
        cls.factory = RequestFactory()

    def test_get(self):
        pass

    def test_post(self):
        request = self.factory.post('/accounts/register/', self.form_data)
        add_middleware_to_request(request, SessionMiddleware)
        request.session.save()
        response = ProfileRegistrationView.as_view()(request)

        # test the newly created account
        try:
            new_user = get_user_model().objects.get(email='a@a.com')
        except ObjectDoesNotExist:
            self.fail("User account a@a.com was not created.")
        self.check_new_user(new_user)

    def test_register(self):
        view = ProfileRegistrationView()
        # setup_view(view, request)
        request = self.factory.get('/accounts/register/')
        add_middleware_to_request(request, SessionMiddleware)
        request.session.save()
        form = CustomUserRegistrationForm(self.form_data)
        new_user = view.register(request, form)
        self.check_new_user(new_user)

    def check_new_user(self, new_user):
        new_profile = new_user.profile
        self.assertEquals(new_user.email, 'a@a.com')
        self.assertTrue(new_user.check_password('pwd'))
        self.assertEquals(new_profile.name, 'Jan')
        self.assertEquals(new_profile.surname, 'Kowalski')

