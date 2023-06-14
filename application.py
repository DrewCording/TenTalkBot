#!/bin/python3 -u
import os
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands
import re
import asyncio

load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('react started on bot {0.user}'.format(client))

@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id == int(os.getenv('welcome_chan')):
        if payload.message_id == int(os.getenv('register_msg')):
            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.remove_reaction(payload.emoji, payload.member)
            if str(payload.emoji.name) == "📩":
                user = message.guild.get_member(payload.user_id)
                verified = discord.utils.get(message.guild.roles, name="Clan Member")
                unverified = discord.utils.get(message.guild.roles, name="unverified")
                category = client.get_channel(int(os.getenv('app_cat')))

                if verified not in user.roles:
                    if unverified in user.roles:
                        index_file = open("react.index", "r")
                        index = index_file.readlines()
                        index_file.close()

                        index = len(index) + 1
                        
                        index_file = open("react.index", "a")
                        index_file.write(str(str(index) + "\n"))
                        index_file.close()

                        app_chan = await message.guild.create_text_channel(str("Application-" + str(index)), category=category)

                        await asyncio.sleep(2)

                        await app_chan.set_permissions(user, read_messages=True, send_messages=True)

                        app_file = open("welcome.msg", "r")
                        await app_chan.send("Hey <@!" + str(user.id) + ">, welcome to **" + user.guild.name + "**!\n\n" + str(app_file.read()))
                        app_file.close()
                
client.run(os.getenv('TOKEN'))

