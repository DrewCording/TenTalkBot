#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('!audit started on bot {0.user}'.format(client))


@client.listen()
async def on_member_remove(member):
    audit_chan = client.get_channel(int(os.getenv('audit_chan')))
    await audit_chan.send("<@!" + str(member.id) + "> (" + member.name + ") has left the server")

@client.listen()
async def on_raw_message_delete(payload):
    audit_chan = client.get_channel(int(os.getenv('audit_chan')))
    if payload.cached_message:
        text = payload.cached_message.content
        user = str(payload.cached_message.author.id)
    else:
        text = "*Message too old to display content*"
        user = "*unkown*"

    await audit_chan.send("A message from <@!" + user + "> was deleted from <#" + str(payload.channel_id) + ">: \n" + text)

client.run(os.getenv('TOKEN'))
