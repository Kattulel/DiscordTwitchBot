# pip install twitch-python
import twitch
import asyncio
import key
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!twitchb ')

helix = twitch.Helix(key.client_id)

connections = []
stream_channel = None
userlist = list()
messages = {"sent": list()}

# Read Channels File
f = open("channels.txt", "r")
channels = f.read().split(",")
f.close()
for name in channels:
    if name != "":
        userlist.append(name)


@bot.event
async def on_ready():
    global connections
    global stream_channel
    connections = bot.guilds
    channels = connections[0].channels

    # find channel
    for i in channels:
        if i.name.lower() == "stream":
            stream_channel = connections[0].get_channel(i.id)  # check if found anyway;
            break
    await run()


# test for name changes
@bot.command()
async def name(ctx, newname):
    await stream_channel.edit(name=newname)


@bot.command()
async def notify(ctx, channel_name):
    f = open("channels.txt", "a+")
    f.write(channel_name+",")
    f.close()
    await ctx.send("Notify OK")


def alreadySent(username):
    if username in messages['sent']:
        return True
    else:
        return False


def sendMessage(username):
    if not alreadySent(username):
        print(username, "is Live.")
        messages['sent'].append(username)


def checkLive():
    for i in userlist:
        user = helix.user(i)
        if user.is_live:
            sendMessage(i)


async def run():
    checkLive()
    await asyncio.sleep(25)
    await run()

bot.run(key.bot_token)
