#!/bin/python3
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
import re

load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('!mention started on bot {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        if message.channel.id == int(os.getenv('channel')):
            pattern = "@(.*?)@"
            pattern2 = "<lt>@!(.*?)<gt>"
            mention = re.search(pattern, message.content)
            mention2 = re.search(pattern2, message.content)
            orig = message.content

            if mention2:
                namestr2 = str("<lt>@!" + mention2.group(1) + "<gt>")
                await message.channel.send(orig.replace(namestr2, str('<@' + str(mention2.group(1)) + '>')))
                await message.delete()
                return

            if mention:
                atuser = mention.group(1)

                for member in message.guild.members:
                    namestr = str("@" + mention.group(1) + "@")
                    if member.nick:
                        nick = member.nick
                        if nick.lower() == atuser.lower():
                            await message.channel.send(orig.replace(namestr, str('<@' + str(member.id) + '>')))
                            await message.delete()
                            break
                    memname = member.name
                    if memname.lower() == atuser.lower():
                        await message.channel.send(orig.replace(namestr, str('<@' + str(member.id) + '>')))
                        await message.delete()
                        break
    else:
        return
client.run(os.getenv('TOKEN'))
