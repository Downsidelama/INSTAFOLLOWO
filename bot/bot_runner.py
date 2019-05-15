import concurrent.futures
import time

from .bot import Bot
from dashboard.models import InstagramAccount

bots = []
executor: concurrent.futures.ThreadPoolExecutor = concurrent.futures.ThreadPoolExecutor(max_workers=100)


def add_bot(instagram_account: InstagramAccount):
    if contains(instagram_account.username) is False:
        bot_runner = BotRunner(
            bot=Bot(instagram_account.username, instagram_account.password),
            run_type=instagram_account.run_type,
            follow_entity=instagram_account.hashtag if instagram_account.run_type == "hashtag"
            else instagram_account.other_profile
        )
        bots.append(bot_runner)
        executor.submit(bot_runner.run)


def contains(name):
    is_containing = any([x for x in bots if x.bot.username == name])
    return is_containing


def is_running(name):
    bot = list(filter(lambda bot: bot.bot.username == name, bots))
    if len(bot) > 0:
        return bot[0].is_running
    return False


def stop(name):
    if contains(name):
        bot = list(filter(lambda b: b.bot.username == name, bots))[0]
        bot.stop()
        bots.remove(bot)
        print(bots)


class BotRunner:

    def __init__(self, bot: Bot, run_type, follow_entity):
        self.bot = bot
        self.type = run_type
        self.follow_entity = follow_entity
        self.is_running = True

    def run(self):
        print("Running bot %s" % self.bot.username)
        while self.is_running:
            if self.type == "hashtag":
                self.bot.follow_by_tag(self.follow_entity)
            else:
                self.bot.follow_by_user_followers(self.bot.get_userid_by_username(self.follow_entity))
            time.sleep(60 * 5)

    def stop(self):
        print("Stopping: " + self.bot.username)
        self.is_running = False


if __name__ == "__main__":
    print("Don't run this module alone!")
