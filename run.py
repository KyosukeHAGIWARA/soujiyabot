# -*- coding: utf-8 -*-

from slackbot.bot import Bot
from slacker import Slacker
import slackbot_settings


def main():
    bot = Bot()
    bot.run()

def search_user_im_id(user_name):
    user_id = ""
    user_im_id = ""
    response = slack.users.list()
    users = response.body["members"]
    for user in users:
        if user["name"] == user_name:
            user_id = user["id"]
            break
    response = slack.im.list()
    ims = response.body["ims"]
    for im in ims:
        if im["user"] == user_id:
            user_im_id = im["id"]
            break
    return user_im_id

if __name__ == "__main__":
    # slack = Slacker(slackbot_settings.API_TOKEN)
    #
    # rawashi_im_id = search_user_im_id("rawashi")
    #
    # slack.chat.post_message(
    #     rawashi_im_id,
    #     "## name : is_bot ##",
    #     as_user=True)
    # for user in users:
    #     slack.chat.post_message(
    #         rawashi_im_id,
    #         str(user["name"]) + " : " + str(user["is_bot"]),
    #         as_user=True)


    main()