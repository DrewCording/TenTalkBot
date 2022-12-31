#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!online started on bot {0.user}'.format(client))


@client.command()
async def online(ctx):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    online_file = open("cc_online.log", "r")

    online_users = ""
    for rsn in online_file:
        online_users = str(online_users + rsn.strip() + ", ")

    if online_users:
        await ctx.channel.send("Currently online in CC: ")
        await ctx.channel.send(online_users)
    else:
        await ctx.channel.send("No users currently online in CC")

client.run(os.getenv('TOKEN'))
