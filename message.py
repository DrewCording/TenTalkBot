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
    print('!message started on bot {0.user}'.format(client))


@client.command()
@commands.has_permissions(manage_roles=True)
async def message(ctx, user: discord.Member, text):
    await user.send(text)


@message.error
async def verify_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide @user to message")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage roles to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !message without permission")

client.run(os.getenv('TOKEN'))

