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
    print('reaction_roles started on bot {0.user}'.format(client))

@client.listen()
async def on_raw_reaction_add(payload):
    channel = client.get_channel(int(os.getenv('channel')))
    if payload.channel_id == int(os.getenv('reactchan')):
        if payload.message_id == int(os.getenv('reactmsg')):
            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = message.guild.get_member(payload.user_id)

            uimrole = discord.utils.get(message.guild.roles, name="UIM")
            hcimrole = discord.utils.get(message.guild.roles, name="HCIM")
            ironrole = discord.utils.get(message.guild.roles, name="Iron")
            hp10role = discord.utils.get(message.guild.roles, name="10HP")
            skillrole = discord.utils.get(message.guild.roles, name="Skiller")
            f2prole = discord.utils.get(message.guild.roles, name="F2P")
            maxrole = discord.utils.get(message.guild.roles, name="Maxed")
            champrole = discord.utils.get(message.guild.roles, name="Champ Cape")

            if str(payload.emoji) == str(os.getenv('uim')):
                if uimrole not in user.roles:
                    print(user, "requested the role UIM")
                    await user.add_roles(uimrole)
    
            elif str(payload.emoji) == str(os.getenv('hcim')):
                if hcimrole not in user.roles:
                    print(user, "requested the role HCIM")
                    await user.add_roles(hcimrole)
    
            elif str(payload.emoji) == str(os.getenv('ironman')):
                if ironrole not in user.roles:
                    print(user, "requested the role Iron")
                    await user.add_roles(ironrole)
    
            elif str(payload.emoji) == str(os.getenv('hp10')):
                if hp10role not in user.roles:
                    print(user, "requested the role 10HP")
                    await user.add_roles(hp10role)
    
            elif str(payload.emoji) == str(os.getenv('skiller')):
                if skillrole not in user.roles:
                    print(user, "requested the role Skiller")
                    await user.add_roles(skillrole)
    
            elif str(payload.emoji) == str(os.getenv('f2p')):
                if f2prole not in user.roles:
                    print(user, "requested the role F2P")
                    await user.add_roles(f2prole)
    
            elif str(payload.emoji) == str(os.getenv('maxed')):
                if maxrole not in user.roles:
                    print(user, "requested the role Maxed")
                    await user.add_roles(maxrole)
    
            elif str(payload.emoji) == str(os.getenv('champ')):
                if champrole not in user.roles:
                    print(user, "requested the role Champ Cape")
                    await user.add_roles(champrole)

            else:
                await message.remove_reaction(payload.emoji, payload.member)

@client.listen()
async def on_raw_reaction_remove(payload):
    channel = client.get_channel(int(os.getenv('channel')))
    if payload.channel_id == int(os.getenv('reactchan')):
        if payload.message_id == int(os.getenv('reactmsg')):
            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = message.guild.get_member(payload.user_id)

            uimrole = discord.utils.get(message.guild.roles, name="UIM")
            hcimrole = discord.utils.get(message.guild.roles, name="HCIM")
            ironrole = discord.utils.get(message.guild.roles, name="Iron")
            hp10role = discord.utils.get(message.guild.roles, name="10HP")
            skillrole = discord.utils.get(message.guild.roles, name="Skiller")
            f2prole = discord.utils.get(message.guild.roles, name="F2P")
            maxrole = discord.utils.get(message.guild.roles, name="Maxed")
            champrole = discord.utils.get(message.guild.roles, name="Champ Cape")

            if str(payload.emoji) == str(os.getenv('uim')):
                if uimrole in user.roles:
                    print(user, "removed the role UIM")
                    await user.remove_roles(uimrole)
    
            elif str(payload.emoji) == str(os.getenv('hcim')):
                if hcimrole in user.roles:
                    print(user, "removed the role HCIM")
                    await user.remove_roles(hcimrole)
    
            elif str(payload.emoji) == str(os.getenv('ironman')):
                if ironrole in user.roles:
                    print(user, "removed the role Iron")
                    await user.remove_roles(ironrole)
    
            elif str(payload.emoji) == str(os.getenv('hp10')):
                if hp10role in user.roles:
                    print(user, "removed the role 10HP")
                    await user.remove_roles(hp10role)
    
            elif str(payload.emoji) == str(os.getenv('skiller')):
                if skillrole in user.roles:
                    print(user, "removed the role Skiller")
                    await user.remove_roles(skillrole)
    
            elif str(payload.emoji) == str(os.getenv('f2p')):
                if f2prole in user.roles:
                    print(user, "removed the role F2P")
                    await user.remove_roles(f2prole)
    
            elif str(payload.emoji) == str(os.getenv('maxed')):
                if maxrole in user.roles:
                    print(user, "removed the role Maxed")
                    await user.remove_roles(maxrole)
    
            elif str(payload.emoji) == str(os.getenv('champ')):
                if champrole in user.roles:
                    print(user, "removed the role Champ Cape")
                    await user.remove_roles(champrole)

client.run(os.getenv('TOKEN'))

