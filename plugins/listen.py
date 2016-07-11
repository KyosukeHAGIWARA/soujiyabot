from slackbot.bot import listen_to

@listen_to("tukareta")
def anzai(message):
    message.send("otu")

@listen_to("harahe")
def reaction(message):
    message.react("+1")
