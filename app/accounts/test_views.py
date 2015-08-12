# coding=utf-8
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.core.exceptions import ObjectDoesNotExist
from django.test import RequestFactory, TestCase

from app.accounts.forms import CustomUserRegistrationForm
from app.accounts.views import ProfileRegistrationView, ProfileUpdateView
from app.main.utils import add_middleware_to_request, setup_view
from app.users.models import Profile


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
        request = self.factory.get('')
        request.user = AnonymousUser()
        response = ProfileRegistrationView.as_view()(request)
        self.assertContains(response, u'Załóż nowe konto')

    def test_post(self):
        request = self.factory.post('', self.form_data)
        request.user = AnonymousUser()
        add_middleware_to_request(request, SessionMiddleware)
        request.session.save()
        response = ProfileRegistrationView.as_view()(request)

        # test the newly created account
        try:
            new_user = get_user_model().objects.get(email='a@a.com')
        except ObjectDoesNotExist:
            self.fail("User account a@a.com was not created.")
        self.check_new_user_is_saved(new_user)

    def test_register(self):
        view = ProfileRegistrationView()
        # setup_view(view, request)
        request = self.factory.get('/accounts/register/')
        add_middleware_to_request(request, SessionMiddleware)
        request.session.save()
        form = CustomUserRegistrationForm(self.form_data)
        new_user = view.register(request, form)
        self.check_new_user_is_saved(new_user)

    def check_new_user_is_saved(self, new_user):
        new_profile = new_user.profile
        self.assertEquals(new_user.email, 'a@a.com')
        self.assertTrue(new_user.check_password('pwd'))
        self.assertEquals(new_profile.name, 'Jan')
        self.assertEquals(new_profile.surname, 'Kowalski')


class TestProfileUpdateView(TestCase):
    @classmethod
    def setUpClass(cls):
        super(TestProfileUpdateView, cls).setUpClass()
        cls.factory = RequestFactory()

    def test_get_form(self):
        user = get_user_model().objects.create_user('a@a.com', 'pwd')
        profile = Profile(user=user, name='Jan', surname='Nowak')
        request = self.factory.get('')
        request.user = user
        request.profile = profile
        view = ProfileUpdateView()
        setup_view(view, request)
        form = view.get_form()
        initial = {
            'email': 'a@a.com',
            'name': 'Jan',
            'surname': 'Nowak',
        }
        self.assertDictEqual(form.initial, initial)
        self.assertIs(form.user, user)
