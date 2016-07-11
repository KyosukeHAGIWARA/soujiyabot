from slackbot.bot import respond_to

@respond_to("hogehoge")
@respond_to("nurupo")
def cheer(message):
    message.reply("ga!")