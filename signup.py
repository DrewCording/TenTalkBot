#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!signup started on bot {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!signup":
        if message.author == client.user:
            if message.channel.id == int(os.getenv('botchan')):
                cc_chan = client.get_channel(int(os.getenv('channel')))
                await cc_chan.send('*Use this in Discord to ping the mods/admins that you would like to join SOTW')
        else:
            if message.author.nick:
                name = message.author.nick
            else:
                name = message.author.name

            await message.channel.send(name + " would like to sign up for SOTW. Please check if they have passed probation and sign them up <@&" + str(os.getenv('leader')) + "> <@&" + str(os.getenv('council')) + ">")
    else:
        return
client.run(os.getenv('TOKEN'))
