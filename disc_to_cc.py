#!/bin/python3 -u
import os
import time
import discord
import random
from dotenv import load_dotenv
from discord.ext import commands
import pyautogui
import re

load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
        print('Disc_to_CC started on bot {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		if message.channel.id == int(os.getenv('channel')):
			content = str(message.content)
			if content.startswith('*'):
				text = str("/" + content[1:])
				await message.delete()
				intv = "0.0" + str(random.randrange(50, 99, 1))
				pyautogui.write(text, interval = intv)
				pyautogui.hotkey('enter')
	else:
		if message.channel.id == int(os.getenv('channel')):
			content = str(message.content)
			
			user_ptrn = "<@!(.*?)>"
			chan_ptrn = "<#(.*?)>"
			emot_ptrn = "<:(.*?)>"
			emot_ptrn_cc = "<:(.*?):"
			
			user_ment = re.search(user_ptrn, content)
			chan_ment = re.search(chan_ptrn, content)
			emot_ment = re.search(emot_ptrn, content)
			emot_ment_cc = re.search(emot_ptrn_cc, content)
			
			if user_ment:
				user_full = str("<@!" + user_ment.group(1) + ">")
				user_name = 0
				user_name = message.guild.get_member(int(user_ment.group(1)))
				
				if user_name:
					if user_name.nick:
						content = content.replace(user_full, str("@" + user_name.nick + "@"))
					else:
						content = content.replace(user_full, str("@" + user_name.name + "@"))
				else:
					user = message.author
					content = content.replace(user_full, str("@???@"))
					await user.send("Warning: You attempted to @ a user that does not exist on <#" + os.getenv('channel') + ">: " + user_full)
				
			if chan_ment:
				chan_full = str("<#" + chan_ment.group(1) + ">")
				chan_name = 0
				chan_name = message.guild.get_channel(int(chan_ment.group(1)))
				
				if chan_name:
					content = content.replace(chan_full, str("#" + chan_name.name + "#"))
				else:
					user = message.author
					content = content.replace(chan_full, str("#???#"))
					await user.send("Warning: You attempted to # a channel that does not exist on <#" + os.getenv('channel') + ">: " + chan_full)
			
			if emot_ment:
				emot_full = str("<:" + emot_ment.group(1) + ">")
				emot_cc = str(":" + str(emot_ment_cc.group(1)) + ":")
				content = content.replace(emot_full, emot_cc)
			
			if message.author.nick:
				text = ("/[" + message.author.nick + "] " + content)
			else:
				text = ("/[" + message.author.name + "] " + content)
					
			if len(text) > 80:
				text = text[:80]
				user = message.author
				await user.send("Warning: Your last message <#" + os.getenv('channel') + "> was too long. Messages are limited to 80 characters including your name")
					
			await message.delete()
			intv = "0.0" + str(random.randrange(50, 99, 1))
			pyautogui.write(text, interval = intv)
			pyautogui.hotkey('enter')
				
client.run(os.getenv('TOKEN'))