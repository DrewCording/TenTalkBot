#!/bin/python3 -u
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
    print('ccbot_commands started on bot {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        if message.channel.id == int(os.getenv('channel')):
            content = str(message.content)
            flag=0
            user_ptrn = "@(.*?)@"
            chan_ptrn = "#(.*?)#"
            user_ment = re.search(user_ptrn, content)
            chan_ment = re.search(chan_ptrn, content)

            if user_ment:
                user_name = user_ment.group(1)

                for member in message.guild.members:
                    user_full = str("@" + user_name + "@")
                    name = member.name
                    if member.nick:
                        nick = member.nick
                        if nick.lower() == user_name.lower():
                            content = content.replace(user_full, str('<@' + str(member.id) + '>'))
                            flag=1
                            break
                    if name.lower() == user_name.lower():
                        content = content.replace(user_full, str('<@' + str(member.id) + '>'))
                        flag=1
                        break

            if chan_ment:
                chan_name = chan_ment.group(1)

                for channel in message.guild.channels:
                    chan_full = str("#" + chan_name + "#")
                    name = channel.name

                    if name.lower() == chan_name.lower():
                        content = content.replace(chan_full, str('<#' + str(channel.id) + '>'))
                        flag = 1
                        break

            cmd_cfg = open("ccbot_commands.cfg", "r")
            bot_chan = client.get_channel(int(os.getenv('botchan')))

            for cmd in cmd_cfg:
                content_l = content.lower()
                cmd_ment = content_l.find(str("!" + cmd.strip()))

                if cmd_ment > 0:
                    await bot_chan.send(str("!" + cmd.strip()))

            cmd_cfg.close()

            if flag:
                await message.channel.send(content)
                await message.delete()
    else:
        return
client.run(os.getenv('TOKEN'))
