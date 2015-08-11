# coding=utf-8
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from app.accounts.forms import ProfileUpdateForm
from app.users.models import Profile


class TestProfileUpdateForm(TestCase):
    def setUp(self):
        super(TestProfileUpdateForm, self).setUp()
        self.user = get_user_model().objects.create_user('a@b.com', 'pwd')
        self.profile = Profile.objects.create(
            name='Jan',
            surname='Nowak',
            user=self.user,
        )

    def test_form_valid_email_changes(self):
        """
        The form should be valid when a new valid email is supplied.
        """
        data = {
            'email': 'e@f.com',
            'name': 'Jan',
            'surname': 'Nowak',
        }
        form = ProfileUpdateForm(instance=self.profile, user=self.user, data=data)
        self.assertTrue(form.is_valid())

    def test_form_valid_when_email_doesnt_change(self):
        """
        The form should be valid when the email doesn't change.
        """
        data = {
            'email': 'a@b.com',
            'name': 'Jan',
            'surname': 'Nowak',
        }
        form = ProfileUpdateForm(instance=self.profile, user=self.user, data=data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_when_email_already_registered(self):
        """
        The form should be invalid when the new email is already registered in NaKranach.pl .
        """

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
        self.assertRegexpMatches(form.errors['email'][0], ur'Email .* jest już zarejestrowany w nakranach')

    def test_form_save(self):
        """
        When data is valid, the new email should be saved to the user model instance.
        """
        data = {
            'email': 'e@f.com',
            'name': 'Jan',
            'surname': 'Nowak',
        }
        form = ProfileUpdateForm(instance=self.profile, user=self.user, data=data)
        form.is_valid()
        form.save()
        self.assertEquals(self.user.email, 'e@f.com')
