from slackbot.bot import respond_to

@respond_to("clean-up")
def cheer(message):
    message.reply("gagaga!")