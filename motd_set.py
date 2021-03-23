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
    print('!motd_set started on bot {0.user}'.format(client))


@client.command()
@commands.has_permissions(manage_messages=True)
async def motd_set(ctx, motd):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    motd_file = open("motd_disc.msg", "w")
    motd_file.write(str(motd))
    motd_file.close()
    await ctx.send("MOTD message set to:")
    motd_file = open("motd_disc.msg", "r")
    await ctx.send(str(motd_file.read()))
    print(ctx.author, "set the motd to", motd)
    motd_file.close()

@motd_set.error
async def move_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide a message to set")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage messages to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !motd_set without permission")

client.run(os.getenv('TOKEN'))

