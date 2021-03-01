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
    print('!welcome_set started on bot {0.user}'.format(client))


@client.command()
@commands.has_permissions(manage_messages=True)
async def welcome_set(ctx, welcome):
    if ctx.channel.id == int(os.getenv('channel')):
        return
    
    welcome_file = open("welcome.msg", "w")
    welcome_file.write(str(welcome))
    welcome_file.close()
    await ctx.send("Discord Welcome message set to:")
    welcome_file = open("welcome.msg", "r")
    await ctx.send("Hey <@!" + str(ctx.message.author.id) + ">, welcome to **" + ctx.guild.name + "**!" + "\n\n" + str(welcome_file.read()))
    #await ctx.send(str(welcome_file.read()))
    print(ctx.author, "set Discord welcome message to", welcome)
    welcome_file.close()
'''
@welcome_set.error
async def welcome_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide a message to set")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage messages to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !welcome_set without permission")
'''
client.run(os.getenv('TOKEN'))

