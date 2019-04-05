import re

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from .models import InstagramAccount


def login(func):
    """
    Logs in at the start of the function and logs out after it finished.
    """

    def inner(self, *a, **kw):
        self.client.login(username='root', password='root')
        func(self, *a, **kw)
        self.client.logout()

    return inner


class DashboardTestCase(TestCase):
    def setUp(self):
        self.client = Client(follow=False)
        self.dummy_user = User.objects.create_user(username="root", password="root")

    def test_index_login_required(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(302, response.status_code)

    def test_profile_login_required(self):
        response = self.client.get('/dashboard/profile/')
        self.assertEqual(302, response.status_code)

    def test_accounts_login_required(self):
        response = self.client.get('/dashboard/accounts/')
        self.assertEqual(302, response.status_code)

    @login
    def test_accounts_list_new_acount(self):
        account = self.create_dummy_ig_account()
        response = self.client.get('/dashboard/accounts/')
        self.assertEqual(1, response.context['account_count'])
        account.delete()

    @staticmethod
    def create_dummy_ig_account():
        account = InstagramAccount()
        account.username = "test_account_ig"
        account.password = "root"
        account.hashtag = ""
        account.started = False
        account.run_type = ""
        account.other_profile = ""
        account.save()
        return account

    @login
    def test_no_ig_account_listing_correct(self):
        response = self.client.get('/dashboard/accounts/')
        self.assertContains(response, 'No accounts yet')

    @login
    def test_index_displays_correct_number_of_accounts(self):
        response = self.client.get('/dashboard/')
        contains_pattern = re.findall(r'Users(.*)1', response.content.decode().strip(), re.MULTILINE | re.DOTALL)
        self.assertTrue(contains_pattern)
