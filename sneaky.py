#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!sneaky started on bot {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!sneaky":
            if message.author == client.user:
                if message.channel.id == int(os.getenv('botchan')):
                    cc_chan = client.get_channel(int(os.getenv('channel')))
                    await cc_chan.send("*Sneaky Teak became the worlds first maxed 10HP iron on January 14, 2023")
                    #await cc_chan.send("*Yes, Jerby is a big meanie.")
            else:
                await message.channel.send("Sneaky Teak became the worlds first maxed 10HP iron on January 14, 2023")
                #await cc_chan.send("Yes, Jerby is a big meanie.")
    else:
        return
client.run(os.getenv('TOKEN'))

