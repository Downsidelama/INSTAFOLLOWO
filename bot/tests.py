from django.test import TestCase
from .bot import Bot

import time
import os


class BotTestCase(TestCase):
    if "TRAVIS" not in os.environ:
        @classmethod
        def setUpTestData(cls):
            cls.username = "instfow1"
            cls.password = "pe1234"
            cls.bot = Bot(cls.username, cls.password)

        def setUp(self):
            if not self.bot.loggedin:
                self.bot.login()

        def test_logged_in(self):
            self.assertTrue(self.bot.loggedin)

        def test_false_login(self):
            bot = Bot("instfow1", "pe12345")
            self.assertFalse(bot.loggedin)

        def test_logout(self):
            self.bot.logout()
            self.assertFalse(self.bot.loggedin)

        def test_get_userdata(self):
            profile = "natgeo"
            username = self.bot.get_userdata(profile)["username"]
            self.assertEquals(username, profile)

        def test_get_userid_by_username(self):
            profile = "natgeo"
            userid = self.bot.get_userid_by_username(self.username)
            userid2 = self.bot.get_userid_by_username(profile)
            self.assertEquals((userid, userid2), (self.bot.user_id, "787132"))

        def test_get_username_by_userid(self):
            username = self.bot.get_username_by_userid(self.bot.user_id)
            username2 = self.bot.get_username_by_userid("787132")
            self.assertEquals((username, username2), (self.username, "natgeo"))

        def test_is_followed_by(self):
            profile_true = "placeholder"  # none:(
            profile_false = "natgeo"
            bool_true = self.bot.is_followed_by(profile_true)
            bool_false = self.bot.is_followed_by(profile_false)
            self.assertEquals((False, False), (bool_true, bool_false))

        def test_is_following(self):
            profile_true = "gopro"
            profile_false = "blabla"
            bool_true = self.bot.is_following(profile_true)
            bool_false = self.bot.is_following(profile_false)
            self.assertEquals((True, False), (bool_true, bool_false))

        def test_follow(self):
            profile = "natgeowild"
            userid = self.bot.get_userid_by_username(profile)
            if self.bot.is_following(profile):
                self.bot.unfollow(userid)
                time.sleep(3)
            self.bot.follow(userid)
            self.assertTrue(self.bot.is_following(profile))

        def test_unfollow(self):
            profile = "natgeowild"
            userid = self.bot.get_userid_by_username(profile)
            if not self.bot.is_following(profile):
                self.bot.follow(userid)
                time.sleep(3)
            self.bot.unfollow(userid)
            self.assertFalse(self.bot.is_following(profile))

        def test_get_mediaids_by_tag(self):
            tag = "hungary"
            array = self.bot.get_mediaids_by_tag(tag)
            self.assertTrue(len(array) > 10)

        def test_get_userids_by_tag(self):
            tag = "hungary"
            array = self.bot.get_userids_by_tag(tag)
            self.assertTrue(len(array) > 10)

        def test_get_followerids(self):
            profile = "natgeo"  # must have atleast 1 follower
            profileid = self.bot.get_userid_by_username(profile)
            userid = self.bot.get_followerids(profileid, 1)
            self.assertEquals(len(userid), 1)

        def test_get_followingids(self):
            profile = "natgeo"  # must have atleast 1 following
            profileid = self.bot.get_userid_by_username(profile)
            userid = self.bot.get_followingids(profileid, 1)
            self.assertEquals(len(userid), 1)
