import os
import time 
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
import pyautogui

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
	print('Disc_to_CC started on bot {0.user}'.format(client))
	
@client.event
async def on_message(message):
	if message.author == client.user:
		return
		
	if message.channel.id == 813255331840524319:
		text = (message.author.nick + ": " + message.content)
                await message.delete()
		intv = "0.0" + str(random.randrange(01, 50, 1))
		pyautogui.hotkey'enter')
		pyautogui.write(text, interval = intv)
		pyautogui.hotkey('enter')

client.run(os.getenv('TOKEN'))
