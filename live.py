#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import twitch
import asyncio

load_dotenv()
helix = twitch.Helix(os.getenv('twitch_client'), os.getenv('twitch_secret'))
client = commands.Bot(command_prefix='+123+')

@client.event
async def on_ready():
        print('Live started on bot {0.user}'.format(client))

async def twitch_live():
    await client.wait_until_ready()
    twitch_channel = client.get_channel(int(os.getenv('twitch_channel')))

    try:
        while 1:
            await asyncio.sleep (1)
            users_file = open("twitch_users.log", "r")
            users = users_file.readlines()
            users_file.close()
            users = [x.replace('\n', '') for x in users]

            live_file = open("twitch_live.log", "r")
            live = live_file.readlines()
            live_file.close()
            live = [x.replace('\n', '') for x in live]
            
            i=0
            twitch_chans = []
            disc_ids = []
            for user in users:
                if i:
                    i=0
                    twitch_chans.append(user)
                else:
                    i=1
                    disc_ids.append(user)

            i=0
            for chan in twitch_chans:
                user = helix.user(chan)
                if user.is_live:
                    if user.display_name not in live:
                        await twitch_channel.send(str("<@!" + disc_ids[i] + "> is live now: **" + user.stream.title + "**\n" + "https://www.twitch.tv/" + user.display_name))
                        live_file = open("twitch_live.log", "a")
                        live_file.write(str(user.display_name + "\n"))
                        live_file.close()
                i=i+1

            live_file = open("twitch_live.log", "r")
            live = live_file.readlines()
            live_file.close()
            live = [x.replace('\n', '') for x in live]

            live_file = open("twitch_live.log", "w")
            for lve in live:
                live_user = helix.user(lve)
                if live_user.is_live:
                    live_file.write(str(live_user.display_name + "\n"))
            live_file.close()

    except: 
        client.loop.create_task(twitch_live())

client.loop.create_task(twitch_live())
client.run(os.getenv('TOKEN'))



