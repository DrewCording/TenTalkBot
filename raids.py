#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!raids started on bot {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!raids":
        if message.author == client.user:
            if message.channel.id == int(os.getenv('botchan')):
                cc_chan = client.get_channel(int(os.getenv('channel')))
                await cc_chan.send('*Use this in Discord for an invite to Level 3 Raids server. Free masses weekly')
        else:
            if message.author.nick:
                name = message.author.nick
            else:
                name = message.author.name

            await message.channel.send("If you are interested in learning CoX Raids on a Level 3 or 10HP, check out the Level 3 Raids Discord Server. Free mass raids every week. Invite link: https://discord.gg/wVSkAABhdr")
    else:
        return
client.run(os.getenv('TOKEN'))
