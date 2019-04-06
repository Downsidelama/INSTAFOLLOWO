import re
from unittest import mock
import socket

from django.contrib.auth.models import User
from django.test import Client
from django.test import TestCase

from .models import InstagramAccount
from .libs.BotSocket import BotSocket
from .libs.BotStatus import BotStatus


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


class BotConnectTest(TestCase):

    def test_set_bot_running_status_running(self):
        with mock.patch('socket.socket') as mock_socket:
            mock_socket.return_value.recv.return_value = 'RUNNING'.encode()
            bs = BotSocket()
            bs.set_account_status("root", BotStatus.RUNNING)
            self.assertEqual(bs.get_account_status("root"), BotStatus.RUNNING)

    @mock.patch('socket.socket')
    def test_set_status_successful_returns_true(self, mock_socket):
        bs = BotSocket()
        self.assertTrue(bs.set_account_status('root', BotStatus.RUNNING))

    @mock.patch.object(socket.socket, 'connect')
    @mock.patch.object(socket.socket, 'sendall', side_effect=socket.error())
    @mock.patch.object(socket.socket, 'recv')
    def test_set_status_unsuccessful_returns_false(self, a, b, c):
        """
        Simulate network error by mocking socket.socket
        :param a:
        :param b:
        :param c:
        :return:
        """
        bs = BotSocket()
        rv = bs.set_account_status('root', BotStatus.RUNNING)
        self.assertFalse(rv)
