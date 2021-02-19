#!/bin/python3
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

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
                return

            if message.embeds:
                embed = message.embeds[0]
                embed.title = f'Embed by: {message.author}'

            else:
                embed = discord.Embed(
                    title=f'Message by: {message.author}',
                    description=message.content
                )

            await channel.send(embed=embed)
            await message.delete()

@move.error
async def move_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide #Channel and message id")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage messages to run this command")

client.run(os.getenv('TOKEN'))
