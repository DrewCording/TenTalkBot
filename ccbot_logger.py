#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
import re

load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('!logger started on bot {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        if message.channel.id == int(os.getenv('channel')):
            print(message.author,":",message.content)

client.run(os.getenv('TOKEN'))

