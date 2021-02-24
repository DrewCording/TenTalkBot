#!/bin/python3 -u 
import os
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
	print('CC_to_Disc started on bot {0.user}'.format(client))
	
async def cc_to_disc():
	await client.wait_until_ready()
	channel = client.get_channel(int(os.getenv('channel')))
	file_to_watch = os.getenv('cclog')
	oldline = " "
	while 1:
			time.sleep (0.5)
			with open(file_to_watch, 'r') as f:
					lines = f.read().splitlines()
					last_line = lines[-1]

			last_line = last_line.replace("<img=2>", os.getenv('ironman'))
			last_line = last_line.replace("<img=3>", os.getenv('uim'))
			last_line = last_line.replace("<img=10>", os.getenv('hcim'))

			if last_line != oldline:
					await channel.send(last_line)

			oldline = last_line

client.loop.create_task(cc_to_disc())
client.run(os.getenv('TOKEN'))
