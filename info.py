#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!info started on bot {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!info":
        if message.author == client.user:
            if message.channel.id == int(os.getenv('botchan')):
                try: 
                    info_file = open("info_cc.msg", "r")
                    info_msg = info_file.read()
                    info_file.close()
                except: 
                    info_msg = "No info message is set"

                cc_chan = client.get_channel(int(os.getenv('channel')))
                await cc_chan.send(str('*' + info_msg))
        else:
            try: 
                info_file = open("info_disc.msg", "r")
                info_msg = info_file.read()
                info_file.close()
            except: 
                info_msg = "No info message is set"

            await message.channel.send(str(info_msg))
    else:
        return
client.run(os.getenv('TOKEN'))

