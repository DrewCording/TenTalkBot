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
    print('!application_set started on bot {0.user}'.format(client))


@client.command()
@commands.has_permissions(manage_messages=True)
async def application_set(ctx, application):
    if len(application) > 1925:
        await ctx.send("Message too long. Max length is 1925 characters, must allow room to @user at start")
        await ctx.send("Your message is " + str(len(application)) + " characters")
    else:
        application_file = open("application.msg", "w")
        application_file.write(str(application))
        application_file.close()
        await ctx.send("Discord Application message set to:")
        application_file = open("application.msg", "r")
        application_msg = str("Hey <@!" + str(ctx.message.author.id) + ">, welcome to **" + ctx.guild.name + "**!" + "\n\n" + str(application_file.read()))
        application_file.close()
        await ctx.send(application_msg)
        print(ctx.author, "set Discord application message to", application)

@application_set.error
async def application_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide a message to set")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage messages to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !application_set without permission")

client.run(os.getenv('TOKEN'))

