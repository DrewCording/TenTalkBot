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
    print('!poll_cancel started on bot {0.user}'.format(client))


@client.command()
#@commands.has_permissions(manage_messages=True)
async def poll_cancel(ctx, poll_num: int):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    if os.path.exists(str("poll" + str(poll_num) + ".tmp")):
        poll_file = open(str("poll" + str(poll_num) + ".tmp"), "r")
        poll_data = poll_file.readlines()
        poll_file.close()

        if str(poll_data[1]).strip() == str(ctx.author.id):
            #os.remove(str("poll" + str(poll_num) + ".tmp"))
            await ctx.send("Cancelled poll #" + str(poll_num) + " by <@!" + str(poll_data[1]).strip() + ">")
        elif ctx.author.guild_permissions.manage_messages:
            #os.remove(str("poll" + str(poll_num) + ".tmp"))
            await ctx.send("Cancelled poll #" + str(poll_num) + " by <@!" + str(poll_data[1]).strip() + ">")
        else:
            await ctx.send("You can only cancel your own polls without mod status.")
            print(str(str(datetime.now()) + str(ctx.author) + " attempted to delete a poll without permission"))
    else:
        await ctx.send("Poll #" + str(poll_num) + " not currently running")
'''
@poll_cancel.error
async def poll_cancel_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide poll number to cancel")
'''
client.run(os.getenv('TOKEN'))
