#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
import twitch

load_dotenv()
client = commands.Bot(command_prefix='!')
helix = twitch.Helix(os.getenv('twitch_client'), os.getenv('twitch_secret'))

@client.event
async def on_ready():
    print('!register started on bot {0.user}'.format(client))


@client.command()
async def register(ctx, twitch_id: str):
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
            await ctx.channel.send("The Twitch channel " + user + " is already registered to <@!" + disc_ids[i] + ">")
            return
        if int(disc_ids[i]) == ctx.author.id:
            await ctx.channel.send("You have already registered the Twitch channel " + user + ".\n Use !unregister to unregister this channel before registering a new one.")
            return
        i=i+1

    new_twitch = helix.user(twitch_id)
    if new_twitch:
        users_file = open("twitch_users.log", "a")
        users_file.write(str(str(ctx.author.id) + "\n"))
        users_file.write(str(twitch_id + "\n"))
        await ctx.channel.send("The Twitch channel " + twitch_id + " is now registered to <@!" + str(ctx.author.id) + ">")
        print(str(str(ctx.author) + " registered the Twitch cahnnel " + new_twitch.display_name))

    else: 
        await ctx.channel.send("The Twitch channel " + twitch_id + " does not exist.")

@register.error
async def register_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide Twitch Channel to register")

client.run(os.getenv('TOKEN'))
