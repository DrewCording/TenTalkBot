#!/bin/python3 -u
import os
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands
import re

load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    print('reaction_roles started on bot {0.user}'.format(client))

async def reaction_roles():
    await client.wait_until_ready()
    channel = client.get_channel(int(os.getenv('channel')))

    react_chan = client.get_channel(int(os.getenv('reactchan')))
    react_msg = await react_chan.fetch_message(int(os.getenv('reactmsg')))

    uimrole = discord.utils.get(react_msg.guild.roles, name="UIM")
    hcimrole = discord.utils.get(react_msg.guild.roles, name="HCIM")
    ironrole = discord.utils.get(react_msg.guild.roles, name="Iron")
    hp10role = discord.utils.get(react_msg.guild.roles, name="10HP")
    skillrole = discord.utils.get(react_msg.guild.roles, name="Skiller")
    f2prole = discord.utils.get(react_msg.guild.roles, name="F2P")
    maxrole = discord.utils.get(react_msg.guild.roles, name="Maxed")
    champrole = discord.utils.get(react_msg.guild.roles, name="Champ Cape")

    while 1:
        for reaction in react_msg.reactions:
            async for user in reaction.users():
                if str(reaction) == str(os.getenv('uim')):
                    if uimrole not in user.roles:
                        print("Making", user, "a UIM")
                        await user.add_roles(uimrole)

                if str(reaction) == str(os.getenv('hcim')):
                    if hcimrole not in user.roles:
                        print(user, "requested the role HCIM")
                        await user.add_roles(hcimrole)

                if str(reaction) == str(os.getenv('ironman')):
                    if ironrole not in user.roles:
                        print(user, "requested the role Iron")
                        await user.add_roles(ironrole)

                if str(reaction) == str(os.getenv('hp10')):
                    if hp10role not in user.roles:
                        print(user, "requested the role 10HP")
                        await user.add_roles(hp10role)

                if str(reaction) == str(os.getenv('skiller')):
                    if skillrole not in user.roles:
                        print(user, "requested the role Skiller")
                        await user.add_roles(skillrole)

                if str(reaction) == str(os.getenv('f2p')):
                    if f2prole not in user.roles:
                        print(user, "requested the role F2P")
                        await user.add_roles(f2prole)

                if str(reaction) == str(os.getenv('maxed')):
                    if maxrole not in user.roles:
                        print(user, "requested the role Maxed")
                        await user.add_roles(maxrole)

                if str(reaction) == str(os.getenv('champ')):
                    if champrole not in user.roles:
                        print(user, "requested the role Champ Cape")
                        await user.add_roles(champrole)

        time.sleep(300)

client.loop.create_task(reaction_roles())
client.run(os.getenv('TOKEN'))

