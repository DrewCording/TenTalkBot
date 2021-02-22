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
	channel = client.get_channel(813255331840524319)
	file_to_watch = os.getenv('cclog')
	oldline = " "
	while 1:
		time.sleep (0.2)
		with open(file_to_watch, 'r') as f:
			lines = f.read().splitlines()
			last_line = lines[-1]
			
		last_line = last_line.replace("<img=2>", "<:ironman:813418947114041385>")
		last_line = last_line.replace("<img=3>", "<:UIM:813418933926232114>")
		last_line = last_line.replace("<img=4>", "<:HCIM:813418921726050314>")
	
		if last_line != oldline:
			await channel.send(last_line)
		
		oldline = last_line

client.run(os.getenv('TOKEN'))
