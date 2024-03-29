#!/bin/python3 -u 
import os
import time
import discord
from dotenv import load_dotenv
from discord.ext import commands
import re
import asyncio

load_dotenv()
client = commands.Bot(command_prefix='+123+')

@client.event
async def on_ready():
	print('CC_to_Disc started on bot {0.user}'.format(client))
	
async def cc_to_disc():
	await client.wait_until_ready()
	channel = client.get_channel(int(os.getenv('channel')))
	file_to_watch = os.getenv('cclog')
	oldline = " "
	login_ptrn_rank = "<col=ef5050>(.*?)</col>"
	login_ment = ""
	
	try:
		while 1:
				await asyncio.sleep (0.2)
				with open(file_to_watch, 'r') as f:
						lines = f.read().splitlines()
						last_line = lines[-1]
				
				login_ment = re.search(login_ptrn_rank, last_line)
				
				if login_ment:
					last_line = str("[Ten Talk] " + login_ment.group(1))
					login_ment = ""
					
				if last_line.endswith("You have left the channel."):
					last_line = "TenTalkBot was disconnected. Attempting to reconnect..."
					
				if last_line.endswith("To talk in your clan's channel, start each line of chat with // or /c."):
					last_line = "TenTalkBot has been reconnected"
					
				last_line = last_line.replace("Â", "")
				last_line = last_line.replace("<img=2>", os.getenv('ironman'))
				last_line = last_line.replace("<img=3>", os.getenv('uim'))
				last_line = last_line.replace("<img=10>", os.getenv('hcim'))
				last_line = last_line.replace("<img=41>", os.getenv('gim'))
				last_line = last_line.replace("<img=22>", "")


				if last_line != oldline:
						await channel.send(last_line)
						oldline = last_line
	except: 
		client.loop.create_task(cc_to_disc())

client.loop.create_task(cc_to_disc())
client.run(os.getenv('TOKEN'))

