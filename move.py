#!/bin/python3
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!move started on bot {0.user}'.format(client))


@client.command()
@commands.has_permissions(manage_messages=True)
async def move(ctx, channel: discord.TextChannel, *message_ids: int):
        for message_id in message_ids:
            message = await ctx.channel.fetch_message(message_id)

            if not message:
                ctx.send("That message id does not exist")
            else:
                await channel.send("**Moved from <#" + str(message.channel.id) + "> -** <@" + str(message.author.id) + ">: " + message.content)
                print(datetime.now())
                print(ctx.author, "moved a message from", message.channel.name, "to", channel.name)
                print(message.author.name, "-", message.content)
                await message.delete()

@move.error
async def move_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide #Channel and message ids")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage messages to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !move without permission")

client.run(os.getenv('TOKEN'))
