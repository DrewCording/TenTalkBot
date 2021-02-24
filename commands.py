#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!discord started on bot {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!commands":
        if message.author == client.user:
            if message.channel.id == int(os.getenv('botchan')):
                cc_chan = client.get_channel(int(os.getenv('channel')))
                    
                cmd_cfg = open("ccbot_commands.cfg", "r")
                cmdlist = "Prefix with !: "
                for cmd in cmd_cfg:
                    cmdlist = str(cmdlist + cmd.strip() + ", ")

                cmd_cfg.close()
                await cc_chan.send(str("*" + cmdlist))
                    
        else:
            cmd_cfg = open("disc_commands.cfg", "r")
            cmdlist = ""
            for cmd in cmd_cfg:
                cmdlist = str(cmdlist + "!" + cmd.strip() + ", ")

            cmd_cfg.close()
            await message.channel.send(cmdlist)
    else:
        return
client.run(os.getenv('TOKEN'))

