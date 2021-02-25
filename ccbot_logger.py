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
    print('ccbot_logger started on bot {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        if message.author == client.user:
            content = str(message.content)
            if content.startswith('*'):
                return
            
            rsn_ptrn = "] (.*?): "
            log_ptrn = "] (.*?) has joined"
            emt_ptrn = "<:(.*?)>"
    
            rsn = re.search(rsn_ptrn, content)
            log = re.search(log_ptrn, content)
            emt = re.search(emt_ptrn, content)
    
            if log:
                cc_logins = open("cc_logins.log", "a")
                cc_logins.write(str(str(log.group(1))+ "\n"))
                cc_logins.close()

            if rsn:
                if emt:
                    emt_full = str("<:" + str(emt.group(1)) + ">")
                    rsn = str(rsn.group(1)).replace(emt_full, "")
                else:
                    rsn = rsn.group(1)

                cc_messages = open("cc_messages.log", "a")
                cc_messages.write(str(rsn + "\n"))
                cc_messages.close()

        else:
            print(message.author,":",message.content)
    else:
        return

client.run(os.getenv('TOKEN'))

