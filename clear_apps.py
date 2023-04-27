#!/bin/python3 -u
import os
from dotenv import load_dotenv
from datetime import date
from datetime import datetime
import re
import time
import discord
from discord.ext import commands
import asyncio

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Clear Apps started on bot {0.user}'.format(client))

async def clear_apps():
    await client.wait_until_ready()
    await asyncio.sleep(1)

    buffer_file = open("old_apps/buffered_apps.log", "r")

    for channel in buffer_file:
        channel_id = str(channel.strip())
        channel_name = client.get_channel(int(channel_id))
        
        if(channel_name):
            await channel_name.delete()
            print(str("Deleted " + str(channel_name) + " at " + str(datetime.now())))

    buffer_file.close()

    os.rename("old_apps/buffered_apps.log", str("old_apps/buffered_apps_" + str(datetime.now()) + ".log"))
    os.rename("open_apps.log", "old_apps/buffered_apps.log")
    
    exit()

client.loop.create_task(clear_apps())
client.run(os.getenv('TOKEN'))
