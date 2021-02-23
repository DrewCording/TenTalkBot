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

        if message.channel.id == int(os.getenv('channel')):
                if message.author.nick:
                    text = (message.author.nick + ": " + message.content)
                else:
                    text = (message.author.name + ": " + message.content)
				
                await message.delete()
                intv = "0.0" + str(random.randrange(50, 99, 1))
                pyautogui.write('/')
                pyautogui.write(text, interval = intv)
                pyautogui.hotkey('enter')
				
client.run(os.getenv('TOKEN'))
