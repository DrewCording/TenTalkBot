#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('welcome started on bot {0.user}'.format(client))


@client.event
async def on_member_join(member):
    welcome_chan = client.get_channel(int(os.getenv('welcome_chan')))

    welcome_file = open("welcome.msg", "r")
    await welcome_chan.send("Hey <@!" + str(member.id) + ">, welcome to **" + member.guild.name + "**!\n\n" + str(welcome_file.read()))
    print(member.name, "joined the server")
    welcome_file.close()

client.run(os.getenv('TOKEN'))

