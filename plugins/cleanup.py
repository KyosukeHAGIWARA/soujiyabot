# -*- coding: utf-8 -*-

import random
import math
import json
import os
from slackbot.bot import respond_to
from slacker import Slacker
import slackbot_settings

slack = Slacker(slackbot_settings.API_TOKEN)


# return list: slack_user_list - (bot_user + duty_free)
def get_duty_member():
    response = slack.users.list()  # users.list API
    all_users = response.body["members"]

    # remove bot
    human_users = []
    for user in all_users:
        if not user["is_bot"]:
            human_users.append(user["name"])

    return list(set(human_users) - set(duty_free))  # calc set difference


# return choice box from unchosen dict
def struct_cb_from_ud(ud, radix):
    # struct next choice_box
    cb = []
    for k, v in ud.items():
        cb += [k for _ in range(math.ceil(radix**v))]
    return cb


# UNIX $uniq -c
def unique(members):
    ans = {}
    for mem in duty_member:
        ans[mem] = 0
    for member in members:
        ans[member] += 1
    return ans


duty_free = ["slackbot"]
duty_member = get_duty_member()


@respond_to("clean-up duty")
@respond_to("cd")
def clean_up_rotation(message):
    radix = 2  # probability ratio

    # load json file and set data
    f = open("./plugins/clean_up.json")
    clean_up_data = json.load(f)
    f.close()
    unchosens_dict = clean_up_data["ud"]
    chosens_list = clean_up_data["chosens_list"]
    choice_box = struct_cb_from_ud(unchosens_dict, radix)

    # choose and post
    choice = random.choice(choice_box)
    chosens_list.append(choice)
    slack.chat.post_message(
        message.body["channel"],
        choice,
        as_user=True)

    # update unchosens_dict
    ud = dict([[key, value+1] for key, value in unchosens_dict.items()])
    ud[choice] -= 1
    # loop back
    while 0 not in ud.values():  # all value vi>=1
        ud = dict([[key, value-1] for key, value in ud.items()])
    unchosens_dict = ud

    # renew json file
    os.remove("./plugins/clean_up.json")
    return_json = {"ud": unchosens_dict, "chosens_list": chosens_list}
    f = open("./plugins/clean_up.json", "w")
    json.dump(return_json, f)
    f.close()

@respond_to("clean-up reset")
def reset_chosen_list(message):
    # load json file and set data
    f = open("./plugins/clean_up.json")
    clean_up_data = json.load(f)
    f.close()
    # reset data
    unchosens_dict = dict([[key, 0] for key, value in clean_up_data["ud"].items()])
    chosens_list = []
    # renew json file
    os.remove("./plugins/clean_up.json")
    return_json = {"ud": unchosens_dict, "chosens_list": chosens_list}
    f = open("./plugins/clean_up.json", "w")
    json.dump(return_json, f)
    f.close()

    slack.chat.post_message(
        message.body["channel"],
        "good bye clean-up list",
        as_user=True)

@respond_to("clean-up statistics")
def post_statistics(message):
    # load json file and set data
    f = open("./plugins/clean_up.json")
    clean_up_data = json.load(f)
    f.close()

    slack.chat.post_message(
        message.body["channel"],
        str(unique(clean_up_data["chosens_list"])),
        as_user=True)
