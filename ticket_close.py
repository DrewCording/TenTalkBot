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
    print('ticket close started on bot {0.user}'.format(client))

@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == client.user.id:
        return

    channel = client.get_channel(payload.channel_id)
    channel_cat = channel.category

    if channel_cat.id == int(os.getenv('ticket_cat')):
        list_file = open("ticket.list", "r")
        ticket_list = list_file.readlines()
        list_file.close()

        ticket_list = list(map(str.strip, ticket_list))

        if str(payload.message_id) in ticket_list:
            await asyncio.sleep(0.3)
            message = await channel.fetch_message(payload.message_id)
            await message.remove_reaction(payload.emoji, payload.member)

            if str(payload.emoji.name) == "🔒":
                ticket_list.remove(str(payload.message_id))

                list_file = open("ticket.list", "w")
                for items in ticket_list: 
                    list_file.write(str(items + "\n"))
                list_file.close()

                await channel.send("This ticket has been closed by <@!" + str(payload.user_id) + ">")
                await channel.edit(name=str("Closed-" + str(channel.name)))

                msg_ptrn = "<@!(.*?)>"
                user_id = re.search(msg_ptrn, message.content)
                user = message.guild.get_member(int(user_id.group(1)))
                await channel.set_permissions(user, read_messages=True, send_messages=False)

client.run(os.getenv('TOKEN'))

