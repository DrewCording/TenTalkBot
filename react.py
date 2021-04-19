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
                verified = discord.utils.get(message.guild.roles, name="verified")
                unverified = discord.utils.get(message.guild.roles, name="unverified")

                if verified not in user.roles:
                    if unverified in user.roles:
                        await channel.send("unverified")

                
                #await channel.send ("No " + str(payload.emoji.name) + " for you <@!" + str(payload.user_id) + ">")

client.run(os.getenv('TOKEN'))

