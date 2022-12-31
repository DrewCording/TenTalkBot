#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!motd started on bot {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!motd":
        if message.author == client.user:
            if message.channel.id == int(os.getenv('botchan')):
                try: 
                    motd_file = open("motd_cc.msg", "r")
                    motd_msg = motd_file.read()
                    motd_file.close()
                except: 
                    motd_msg = "No motd is set"

                cc_chan = client.get_channel(int(os.getenv('channel')))
                await cc_chan.send(str('*' + motd_msg))
        else:
            try: 
                motd_file = open("motd_disc.msg", "r")
                motd_msg = motd_file.read()
                motd_file.close()
            except: 
                motd_msg = "No motd is set"

            await message.channel.send(str(motd_msg))
    else:
        return
client.run(os.getenv('TOKEN'))

