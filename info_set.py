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
    print('!info_set started on bot {0.user}'.format(client))


@client.command()
@commands.has_permissions(manage_messages=True)
async def info_set(ctx, info):
    if ctx.channel.id == int(os.getenv('channel')):
        return
    
    info_file = open("info_disc.msg", "w")
    info_file.write(str(info))
    info_file.close()
    await ctx.send("Info message set to:")
    info_file = open("info_disc.msg", "r")
    await ctx.send(str(info_file.read()))
    print(ctx.author, "set info message to", info)
    info_file.close()

@info_set.error
async def move_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide a message to set")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage messages to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !info_set without permission")

client.run(os.getenv('TOKEN'))

