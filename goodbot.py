#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!goodbot started on bot {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!goodbot":
        if message.author == client.user:
            if message.channel.id == int(os.getenv('botchan')):
                cc_chan = client.get_channel(int(os.getenv('channel')))
                await cc_chan.send('*beep boop')
        else:
            await message.channel.send('beep boop')
    else:
        return
client.run(os.getenv('TOKEN'))
