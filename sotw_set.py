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
    print('!sotw_set started on bot {0.user}'.format(client))


@client.command()
@commands.has_permissions(manage_messages=True)
async def sotw_set(ctx, sotw):
    if len(sotw) > 79:
        await ctx.send("Message too long. Character limit is 79 due to in-game use")
    else:
        sotw_file = open("sotw.msg", "w")
        sotw_file.write(str(sotw))
        sotw_file.close()
        await ctx.send("SOTW message set to:")
        sotw_file = open("sotw.msg", "r")
        await ctx.send(str(sotw_file.read()))
        sotw_file.close()

@sotw_set.error
async def move_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide a message to set")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage messages to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !sotw_set without permission")

client.run(os.getenv('TOKEN'))

