#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!discord started on bot {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!discord":
            if message.author == client.user:
                if message.channel.id == int(os.getenv('botchan')):
                    cc_chan = client.get_channel(int(os.getenv('channel')))
                    #await cc_chan.send('*Head to www tentalkosrs com for a Discord invite')
                    await cc_chan.send('*Ten Talk Clan: Discord gg / TPKmAyBQ2R')
            else:
                #await message.channel.send('Head to https://www.tentalkosrs.com for a Discord invite')
                await message.channel.send('*Ten Talk Clan: Discord gg / TPKmAyBQ2R')
    else:
        return
client.run(os.getenv('TOKEN'))

