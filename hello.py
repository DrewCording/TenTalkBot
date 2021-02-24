#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!hello started on bot {0.user}'.format(client))


@client.command()
async def hello(ctx):
    await ctx.send('Hello!')

client.run(os.getenv('TOKEN'))
