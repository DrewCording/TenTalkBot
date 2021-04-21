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
    print('unverify started on bot {0.user}'.format(client))


@client.event
async def on_member_join(member):
    unverified = discord.utils.get(member.guild.roles, name="unverified")
    await member.add_roles(unverified)

client.run(os.getenv('TOKEN'))

