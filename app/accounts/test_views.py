# coding=utf-8
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase, RequestFactory
from app.accounts.forms import CustomUserRegistrationForm, ProfileUpdateForm

from app.accounts.views import ProfileRegistrationView, ProfileUpdateView
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

    def setUp(self):
        self.user = get_user_model().objects.create('a@a.com', 'pwd')

    def test_context(self):
        request = self.factory.get('')
        request.user = self.user
        response = ProfileUpdateView.as_view()(request)
        self.assertIsInstance(response.context['email_name'], ProfileUpdateForm)
        self.assertIsInstance(response.context['password_change'], PasswordChangeForm)

    def test_create_email_name_form(self):
        request = self.factory.get('')
        request.user = self.user
        view = ProfileUpdateView()
        setup_view(view, request)
        form = view.create_email_name_form()

    def test_create_password_change_form(self):
        self.fail()

    def test_email_name_form_valid(self):
        self.fail()

    def test_password_change_form_valid(self):
        self.fail()
