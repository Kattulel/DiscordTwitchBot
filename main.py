# pip install twitch-python
import twitch
import asyncio
import key

helix = twitch.Helix(key.client_id)

userlist = list()
messages = {"sent": list()}

# Read Channels File
f = open("channels.txt", "r")
channels = f.read().split(",")
f.close()
for name in channels:
    userlist.append(name)


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
        sendMessage(i)


async def run():
    while True:
        checkLive()
        await asyncio.sleep(5)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

