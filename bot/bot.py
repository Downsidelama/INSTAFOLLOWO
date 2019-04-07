import requests
import random
import re
import time
import json

#teszt fiok:
#gmail.hu instafollowo pe1234
#instagram instfow1 pe1234

class Bot:

    #Urls
    url_base = "https://www.instagram.com"

    url_login = url_base + "/accounts/login/ajax/"
    url_logout = url_base + "/accounts/logout/"

    #username
    url_profile = url_base + "/{}/"

    #userid
    url_follow = url_base + "/web/friendships/{}/follow/"
    url_unfollow = url_base + "/web/friendships/{}/unfollow/"

    url_api = "https://i.instagram.com/api/v1/users/{}/info/"

    #username
    url_profile = url_base + "/{}"
    url_profile_json = url_profile + "/?__a=1"

    #mediaid
    url_like = url_base + "/web/likes/{}/like/"
    url_unlike = url_base + "/web/likes/{}/unlike/"

    #tag
    #maxid?
    url_media_by_tag = url_base + "/explore/tags/{}/?__a=1"
    url_media_by_tag_maxid = url_base + "/explore/tags/{}/?__a=1&max_id={}/"

    #userid, first(amount)
    #after?
    url_following = url_base + "/graphql/query/?query_id=17874545323001329&id={}&first={}"
    url_following_after = url_base + "/graphql/query/?query_id=17874545323001329&id={}&first={}&after={}"

    url_followers = url_base + "/graphql/query/?query_id=17851374694183129&id={}&first={}"
    url_followers_after = url_base + "/graphql/query/?query_id=17851374694183129&id={}&first={}&after={}"


    #Fake headers
    #TODO: add fake_useragent maybe
    headers_list = [
        "Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101"\
        " Firefox/41.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)"\
        " AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2"\
        " Safari/601.3.9",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0)"\
        " Gecko/20100101 Firefox/15.0.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"\
        " (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36"\
        " Edge/12.246"
    ]


    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.userid = 0
        self.user_agent = self.headers_list[random.randrange(0,4)]

        self.loggedin = False
        self.session = requests.Session()

        #self.followercount = 0
        #self.followingcount = 0

        self.login()


    #TODO: more exception checks
    def login(self):

        self.session.headers.update(
            {
            "Referer": self.url_base,
            "User-Agent": self.user_agent
            }
        )

        self.login_data = {
            "username": self.username,
            "password": self.password
        }

        info = self.session.get(self.url_base)
        csrf_token = re.search('(?<="csrf_token":")\w+', info.text).group(0)
        self.session.headers.update({"X-CSRFToken": csrf_token})

        login = self.session.post(self.url_login, data = self.login_data, allow_redirects = True)
        try:
            self.session.headers.update({"X-CSRFToken": login.cookies["csrftoken"]})
            self.csrftoken = login.cookies["csrftoken"]
        except:
            print("Login error")

        login_json = login.json()

        if (login_json.get("authenticated") and login.status_code == 200):
            print("Successful login!")
            self.loggedin = True
            self.session.cookies["csrftoken"] = csrf_token
            self.userid = self.get_userid_by_username(self.username)
        else:
            print("Login error")

    def logout(self):
        if self.loggedin:
            logout_data = {'csrfmiddlewaretoken': self.csrftoken}
            self.session.post(self.url_logout, data=logout_data)
            self.loggedin = False
            print("Logged out")
        else:
            print("Not logged in")

    
    def get_userdata(self, username):
        url_profile = self.url_profile_json.format(username)

        info = self.session.get(url_profile)
        user_data = json.loads(info.text)["graphql"]["user"]

        return user_data

    def follow(self, userid):
        url_follow = self.url_follow.format(userid)

        if self.loggedin:
            follow = self.session.post(url_follow)

            if follow.status_code == 200:
                #self.followercount += 1
                print("Followed " + userid)

    def unfollow(self, userid):
        url_unfollow = self.url_unfollow.format(userid)

        if self.loggedin:
            unfollow = self.session.post(url_unfollow)

            if unfollow.status_code == 200:
                #self.followercount -= 1
                print("Unfollowed " + userid)

    def like(self, mediaid):
        url_like = self.url_like.format(mediaid)

        if self.loggedin:
            like = self.session.post(url_like)
            print("Liked " + mediaid)

    def unlike(self, mediaid):
        url_unlike = self.url_unlike.format(mediaid)

        if self.loggedin:
            like = self.session.post(url_unlike)
            print("Unliked " + mediaid)

    def is_followed_by(self, username):
        # checks if target profile follows active profile
        user_info = self.get_userdata(username)

        follows_viewer = user_info["follows_viewer"]
        has_requested_viewer = user_info["has_requested_viewer"]

        if (follows_viewer or has_requested_viewer):
            print("Followed by " + username)
            return True
        else:
            print("Not followed by " + username)
            return False

    def is_following(self, username):
        # checks if active profile follows target profile
        user_info = self.get_userdata(username)

        followed_by_viewer = user_info["followed_by_viewer"]
        requested_by_viewer = user_info["requested_by_viewer"]

        if (followed_by_viewer or requested_by_viewer):
            print("Following " + username)
            return True
        else:
            print("Not following " + username)
            return False

    def get_username_by_userid(self, userid):
        # this link may get deprecated 
        url_api = self.url_api.format(userid)
        info = self.session.get(url_api)
        username = json.loads(info.text)["user"]["username"]

        return username

    def get_userid_by_username(self, username):
        user_info = self.get_userdata(username)
        userid = user_info["id"]

        return userid

    def get_mediaids_by_tag(self, tag):
        # returns around 70 mediaids by a hashtag
        url_media_by_tag = self.url_media_by_tag.format(tag)
        mediaids_by_tag = []

        if self.loggedin:
            i = self.session.get(url_media_by_tag)
            media_data = json.loads(i.text)["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
            for i in range(len(media_data)):
                mediaids_by_tag.append((media_data[i]["node"]["id"]))

        return mediaids_by_tag

    def get_userids_by_tag(self, tag):
        # returns around 70 userids by a hashtag
        url_media_by_tag = self.url_media_by_tag.format(tag)
        userids_by_tag = []

        if self.loggedin:
            i = self.session.get(url_media_by_tag)
            media_data = json.loads(i.text)["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"]
            for i in range(len(media_data)):
                userids_by_tag.append((media_data[i]["node"]["owner"]["id"]))

        return userids_by_tag

    def get_followerids(self, userid, amount = 50):
        # returns a maximum of 50 userids that follow target profile
        # seems to actually return less than 50 in most cases for some reason
        # rate_limited error occurs after around 20 requests but resumes inside ~30 mins(?)
        url_followers = self.url_followers.format(userid, amount)
        follower_ids = []
        info = self.session.get(url_followers)
        try:
            followers_data = json.loads(info.text)["data"]["user"]["edge_followed_by"]["edges"]
            for i in range(len(followers_data)):
                follower_ids.append(followers_data[i]["node"]["id"])
        except KeyError:
            print("ERROR: " + json.loads(info.text)["message"])

        return follower_ids
    
    def get_followingids(self, userid, amount = 50):
        # returns userids that target profile is following
        url_followings = self.url_following.format(userid, amount)
        following_ids = []
        info = self.session.get(url_followings)
        try:
            following_data = json.loads(info.text)["data"]["user"]["edge_follow"]["edges"]
            for i in range(len(following_data)):
                following_ids.append(following_data[i]["node"]["id"])
        except KeyError:
            print("ERROR: " + json.loads(info.text)["message"])

        return following_ids 

    def unfollow_if_no_followback(self):
        # unfollows up to 50 profiles that dont follow active profile
        userids = self.get_follower_ids(self.userid)
        for i in range(len(userids)):
            if not self.is_followed_by(userids[i]):
                self.unfollow(userids[i])

    def follow_by_tag(self, tag):
        # TODO: add limits to not get detected as a bot
        userids = self.get_userids_by_tag(tag)
        for i in range(len(userids)):
            self.follow(userids[i])

    def follow_by_user_followers(self, userid):
        # TODO: add limits to not get detected as a bot
        userids = self.get_followerids(userid)
        for i in range(len(userids)):
            self.follow(userids[i])

    def like_by_tag(self, tag):
        # TODO: add limits to not get detected as a bot
        mediaids = self.get_mediaids_by_tag(tag)
        for i in range(len(mediaids)):
            self.like(mediaids[i])