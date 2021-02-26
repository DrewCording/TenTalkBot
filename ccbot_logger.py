#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from discord.utils import get
import re
import time
import asyncio

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
            login_ptrn = "] (.*?) has joined"
            logot_ptrn = "] (.*?) has left"
            emt_ptrn = "<:(.*?)>"
    
            rsn = re.search(rsn_ptrn, content)
            login = re.search(login_ptrn, content)
            logot = re.search(logot_ptrn, content)
            emt = re.search(emt_ptrn, content)
    
            if login:
                cc_logins = open("cc_logins.log", "a")
                cc_logins.write(str(str(login.group(1)) + "\n"))
                cc_logins.close()

                cc_online = open("cc_online.log", "a")
                cc_online.write(str(str(login.group(1)) + "\n"))
                cc_online.close()

                await asyncio.sleep(15)
                await message.delete()

            if logot:
                cc_online = open("cc_online.log", "r")
                cc_online_content = cc_online.readlines()
                cc_online.close()

                cc_online = open("cc_online.log", "w")
                for logout_rsn in cc_online_content:
                    if logout_rsn.strip() != logot.group(1):
                        cc_online.write(logout_rsn)
                cc_online.close()

                await asyncio.sleep(15)
                await message.delete()

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

