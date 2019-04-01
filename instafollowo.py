import requests
import random
import re
import time
import json

class INSTAFOLLOWOBOT:

    #Urls
    url_base = "https://www.instagram.com"

    url_login = url_base + "/accounts/login/ajax/"
    url_logout = url_base + "/accounts/logout/"

    url_profile = url_base + "/{}/"

    # Fake headers
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
        self.user_agent = self.headers_list[random.randrange(0,4)]

        self.session = requests.Session()

    

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


        # finding csrftoken
        r = self.session.get(self.url_base)
        csrf_token = re.search('(?<="csrf_token":")\w+', r.text).group(0)
        self.session.headers.update({"X-CSRFToken": csrf_token})
        time.sleep(5 * random.random())

        login = self.session.post(self.url_login, data = self.login_data, allow_redirects = True)
        login_json = login.json()

        if (login_json.get("authenticated") is True):
            print("Successful login!")
            self.session.cookies["csrftoken"] = csrf_token
        else:
            print("Login error")

    #def logout(self):

        #logout_data = 
        #logout = self.session.post(self.url_logout, data=logout_data)


    def get_data(self):
        url_myprofile = self.url_profile.format(self.username)

        i = self.session.get(url_myprofile)
        json_data = json.loads(
            re.search(
                "window._sharedData = (.*?);</script>", i.text, re.DOTALL
            ).group(1)
        )["entry_data"]["ProfilePage"][0]

        user_data = json_data["graphql"]["user"]

        current_username = user_data["username"]
        followers = user_data["edge_followed_by"]["count"]
        following = user_data["edge_follow"]["count"]


        print("Logged in as {} with {} followers and following {}".format(current_username, followers, following))




bot = INSTAFOLLOWOBOT("123", "123")
bot.login()
bot.get_data()