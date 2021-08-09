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
    print('ticket started on bot {0.user}'.format(client))

@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id == client.user.id:
        return

    if payload.channel_id == int(os.getenv('ticket_chan')):
        if payload.message_id == int(os.getenv('ticket_msg')):
            channel = client.get_channel(payload.channel_id)
            await asyncio.sleep(0.3)
            message = await channel.fetch_message(payload.message_id)
            await message.remove_reaction(payload.emoji, payload.member)
            if str(payload.emoji.name) == "📩":
                user = message.guild.get_member(payload.user_id)
                category = client.get_channel(int(os.getenv('ticket_cat')))

                index_file = open("ticket.index", "r")
                index = index_file.readlines()
                index_file.close()

                index = len(index) + 1
                        
                index_file = open("ticket.index", "a")
                index_file.write(str(str(index) + "\n"))
                index_file.close()

                ticket_chan = await message.guild.create_text_channel(str("Ticket-" + str(index)), category=category)
                await ticket_chan.set_permissions(user, read_messages=True, send_messages=True)

                ticket_file = open("ticket.msg", "r")
                ticket_message = await ticket_chan.send("Hey <@!" + str(user.id) + ">, you have created a new ticket.\n\n" + str(ticket_file.read()))
                ticket_file.close()

                list_file = open("ticket.list", "a")
                list_file.write(str(str(ticket_message.id) + "\n"))
                list_file.close()

                await ticket_message.add_reaction("🔒")
                await ticket_message.pin()
                
client.run(os.getenv('TOKEN'))

