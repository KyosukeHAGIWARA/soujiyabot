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
    users = response.body["members"]

    human_users = []
    for user in users:
        if not user["is_bot"]:
            human_users.append(user["name"])

    member = list(set(human_users) - set(duty_free))
    return member


# return fixed unchosen_list, choice_box
def struct_choice_box(chosen, unchosen_dict, radix):
    # update ud
    ud = dict([[k, v+1] for k, v in unchosen_dict.items()])
    ud[chosen] -= 1

    # loop back
    while 0 not in ud.values():
        ud = dict([[k, v-1] for k, v in ud.items()])

    # struct next choice_box
    cb = struct_cb_from_ud(ud, radix)

    return ud, cb


# return cb
def struct_cb_from_ud(ud, radix):
    # struct next choice_box
    cb = []
    for k, v in ud.items():
        cb += [k for _ in range(math.ceil(radix**v))]
    return cb


# UNIX uniq -c
def unique(members):
    ans = {}
    for mem in duty_member:
        ans[mem] = 0
    for member in members:
        ans[member] += 1
    return ans

duty_free = []
duty_member = get_duty_member()


@respond_to("clean-up")
def clean_up_rotation(message):
    radix = 2

    # json load
    f = open("./plugins/clean_up.json")
    clean_up_data = json.load(f)
    f.close()

    unchosen_dict = clean_up_data["ud"]
    choices = clean_up_data["choices"]
    choice_box = struct_cb_from_ud(unchosen_dict, radix)

    # choose and post
    choice = random.choice(choice_box)
    choices.append(choice)
    unchosen_dict, choice_box = struct_choice_box(choice, unchosen_dict, radix)
    slack.chat.post_message(
        "bot_test",
        choice,
        as_user=True)

    # json overwrite
    os.remove("./plugins/clean_up.json")
    return_json = {"ud": unchosen_dict, "choices": choices}
    f = open("./plugins/clean_up.json", "w")
    json.dump(return_json, f)
    f.close()
