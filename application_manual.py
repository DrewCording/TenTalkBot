#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
import asyncio

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!application started on bot {0.user}'.format(client))


@client.command()
@commands.has_permissions(manage_roles=True)
async def application(ctx, user: discord.Member):
    message = await ctx.channel.fetch_message(ctx.message.id)
    verified = discord.utils.get(message.guild.roles, name="verified")
    unverified = discord.utils.get(message.guild.roles, name="unverified")
    category = client.get_channel(int(os.getenv('app_cat')))

    if verified not in user.roles:
        if unverified in user.roles:
            index_file = open("react.index", "r")
            index = index_file.readlines()
            index_file.close()

            index = len(index) + 1
                        
            index_file = open("react.index", "a")
            index_file.write(str(str(index) + "\n"))
            index_file.close()

            app_chan = await message.guild.create_text_channel(str("Application-" + str(index)), category=category)
            await app_chan.set_permissions(user, read_messages=True, send_messages=True)

            app_file = open("application.msg", "r")
            await app_chan.send("Hey <@!" + str(user.id) + ">, welcome to **" + user.guild.name + "**!\n\n" + str(app_file.read()))
            app_file.close()

        else: 
            await ctx.send("That user is neither verified nor unverified. How did this happen? Please help computer.")

    else:
        await ctx.send("That user is already verified")



@application.error
async def verify_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide @user to open application for")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage roles to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !application without permission")

client.run(os.getenv('TOKEN'))

