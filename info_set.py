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
async def info_set(ctx, typ, info):
    if ctx.channel.id == int(os.getenv('channel')):
        return
    
    if typ.lower() == "discord":
        info_file = open("info_disc.msg", "w")
        info_file.write(str(info))
        info_file.close()
        await ctx.send("Info Discord message set to:")
        info_file = open("info_disc.msg", "r")
        await ctx.send(str(info_file.read()))
        print(ctx.author, "set Discord info message to", info)
        info_file.close()

    elif typ.lower() == "cc":
        if len(info) > 79:
            await ctx.send("Message too long. Character limit is 79 for info cc message")
            await ctx.send(str("Your message is " + str(len(info)) + " characters"))
        else:
            info_file = open("info_cc.msg", "w")
            info_file.write(str(info))
            info_file.close()
            await ctx.send("Info CC message set to:")
            info_file = open("info_cc.msg", "r")
            await ctx.send(str(info_file.read()))
            print(ctx.author, "set CC info message to", info)
            info_file.close()

    else: 
        await ctx.send("Info type not valid. Specify either 'cc' or 'discord'")

@info_set.error
async def move_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide a message to set")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage messages to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !info_set without permission")

client.run(os.getenv('TOKEN'))

