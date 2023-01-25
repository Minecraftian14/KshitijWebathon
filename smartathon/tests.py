import json

from . import models
from .views import ProperException

from django.urls import reverse
from django.test import TestCase


class WelcomingWorldTests(TestCase):
    def test_hello_world(self):
        """

        """
        self.assertTrue(True)
        self.assertEqual("HW", "HW")


class CreateUserCommandTests(TestCase):
    def create_a_user(self, kwargs=None):
        if kwargs is None:
            content = self.client.post(reverse('smartathon:create user service')).content
        else:
            content = self.client.post(reverse('smartathon:create user service'), kwargs).content
        return json.loads(content)

    def test_no_data_or_from_data_method(self):
        res = self.create_a_user()
        self.assertEqual(res['reason'], 'server did not receive any key named name')

    def test_non_alphanumeric_names_or_verify_name_method(self):
        res = self.create_a_user({'name': 'abc'})
        self.assertEqual(res['reason'], 'names smaller than or equal to 5 characters are reserved')
        res = self.create_a_user({'name': 'abc@141516'})
        self.assertEqual(res['reason'], 'only alphanumeric characters and spaces are allowed as names')

    def test_taken_username(self):
        res = self.create_a_user({'name': 'abc141516', 'password': 'anAwes0meP@ssword',
                                  'mail': 'myEmail1234@gmail.com'})
        self.assertEqual(res['status'], 'success')
        res = self.create_a_user({'name': 'abc141516'})
        self.assertEqual(res['reason'], 'username is already in use')

    def test_password(self):
        msg = '''
                invalid password, the password must contain at least one digit, at least one capital case
                character, at least one lower case character and at least one special symbol (@$!%*#?&)
                '''
        # too short
        res = self.create_a_user({'name': 'a valid name',
                                  'password': 'abcd'})
        self.assertEqual(res['reason'], msg)
        # no numbers
        res = self.create_a_user({'name': 'a valid name',
                                  'password': 'abcdefgh'})
        self.assertEqual(res['reason'], msg)
        # no caps
        res = self.create_a_user({'name': 'a valid name',
                                  'password': 'abcd1234'})
        self.assertEqual(res['reason'], msg)
        # no smalls
        res = self.create_a_user({'name': 'a valid name',
                                  'password': 'ABCD1234'})
        self.assertEqual(res['reason'], msg)
        # no specials
        res = self.create_a_user({'name': 'a valid name',
                                  'password': 'ABcd1234'})
        self.assertEqual(res['reason'], msg)
        # should pass
        res = self.create_a_user({'name': 'a valid name',
                                  'password': 'ABcd@!34', 'mail': 'a@Valid.Mail'})
        self.assertEqual(res['status'], 'success')

    def test_mail(self):
        res = self.create_a_user({'name': 'a valid name', 'password': 'ABcd@!34',
                                  'mail': '...'})
        self.assertEqual(res['reason'], 'invalid mail format')
