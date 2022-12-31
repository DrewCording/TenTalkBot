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
    print('!unregister started on bot {0.user}'.format(client))


@client.command()
async def unregister(ctx, twitch_id: str):
    if ctx.channel.id == int(os.getenv('channel')):
        return
    
    users_file = open("twitch_users.log", "r")
    users = users_file.readlines()
    users_file.close()
    users = [x.replace('\n', '') for x in users]

    i=0
    twitch_chans = []
    disc_ids = []
    for user in users:
        if i:
            i=0
            twitch_chans.append(user)
        else:
            i=1
            disc_ids.append(user)

    i=0
    for user in twitch_chans:
        if twitch_id.lower() == user.lower():
            if int(disc_ids[i]) == ctx.author.id:
                users_file = open("twitch_users.log", "r")
                users = users_file.readlines()
                users_file.close()
                users = [x.replace('\n', '') for x in users]

                users_file = open("twitch_users.log", "w")
                for twitch_user in users:
                    if user.lower() != twitch_user.lower():
                        if disc_ids[i] != twitch_user:
                            users_file.write(str(twitch_user + "\n"))
                users_file.close()

                await ctx.channel.send("The Twitch channel " + user + " has been unregistered from <@!" + disc_ids[i] + ">")
                return

            elif ctx.author.guild_permissions.manage_messages:
                users_file = open("twitch_users.log", "r")
                users = users_file.readlines()
                users_file.close()
                users = [x.replace('\n', '') for x in users]

                users_file = open("twitch_users.log", "w")
                for twitch_user in users:
                    if user.lower() != twitch_user.lower():
                        if disc_ids[i] != twitch_user:
                            users_file.write(str(twitch_user + "\n"))
                users_file.close()

                await ctx.channel.send("The Twitch channel " + user + " has been unregistered from <@!" + disc_ids[i] + ">")
                return

            else:
                await ctx.channel.send("The Twitch channel " + user + " is registered to <@!" + disc_ids[i] + ">\nYou cannot unregister someone elses channel")
                return

        i=i+1

    await ctx.channel.send("The twitch channel " + twitch_id + " is not registered.")

'''
@unregister.error
async def unregister_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide Twitch Channel to unregister")
'''
client.run(os.getenv('TOKEN'))
