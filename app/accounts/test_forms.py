# coding=utf-8
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from app.accounts.forms import ProfileUpdateForm
from app.users.models import Profile


class TestProfileUpdateForm(TestCase):
    def setUp(self):
        super(TestProfileUpdateForm, self).setUp()
        self.user = get_user_model().objects.create_user('a@b.com, pwd')
        self.profile = Profile.objects.create(
            name='Jan',
            surname='Nowak',
            user=self.user,
        )

    def form_valid_email_changes(self):
        data = {
            'email': 'e@f.com',
            'name': 'Jan',
            'surname': 'Nowak',
        }
        form = ProfileUpdateForm(instance=self.profile, user=self.user, data=data)
        self.assertTrue(form.is_valid())

    def test_form_valid_when_email_doesnt_change(self):
        data = {
            'email': 'a@b.com',
            'name': 'Jan',
            'surname': 'Nowak',
        }
        form = ProfileUpdateForm(instance=self.profile, user=self.user, data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_email_already_registered(self):
        # create second user
        get_user_model().objects.create_user('c@d.com', 'pwd')

        # data now has email which is already registered
        data = {
            'email': 'c@d.com',
            'name': 'Jan',
            'surname': 'Nowak',
        }
        form = ProfileUpdateForm(instance=self.profile, user=self.user, data=data)
        self.assertFalse(form.is_valid())
        # TODO test exception

    def test_form_save(self):
        data = {
            'email': 'e@f.com',
            'name': 'Jan',
            'surname': 'Nowak',
        }
        form = ProfileUpdateForm(instance=self.profile, user=self.user, data=data)
        form.is_valid()
        form.save()
        self.assertEquals(self.user.email, 'e@f.com')
