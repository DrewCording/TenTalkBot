#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from OSRSBytes import Hiscores
from PIL import Image, ImageFont, ImageDraw

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!stats started on bot {0.user}'.format(client))

@client.command()
async def stats(ctx, rsn):
    if ctx.channel.id == int(os.getenv('channel')):
        return
    
    rsn_nospace = rsn.replace(" ","%20")
    print(ctx.message.author, "requested stats for RSN", rsn)
    await ctx.send("Looking up stats for RSN " + str(rsn))
    try: 
        main_stats = Hiscores(rsn_nospace, 'N')
    except: 
        await ctx.send("RSN " + rsn + " not found on highscores")
        await ctx.send("If the RSN contains spaces, put quotes around it, eg \"Test RSN\"")
        main_stats = 0

    if main_stats:
        try:
            iron_stats = Hiscores(rsn_nospace, 'IM')
        except:
            iron_stats = 0

        if iron_stats:
            try:
                uim_stats = Hiscores(rsn_nospace, 'UIM')
            except:
                uim_stats = 0

            if uim_stats:
                await ctx.send(rsn + " is a " + os.getenv('uim'))
            else:
                try:
                    hci_stats = Hiscores(rsn_nospace, 'HIM')
                except:
                    hci_stats = 0

                if hci_stats:
                    if hci_stats.skill('total', 'level') < iron_stats.skill('total', 'level'):
                        await ctx.send(rsn + " is a " + os.getenv('ironman') + " (dead " + os.getenv('hcim') + ")")
                    else:
                        await ctx.send(rsn + " is a " + os.getenv('hcim'))
                else:
                    await ctx.send(rsn + " is a " + os.getenv('ironman'))
        else:
            await ctx.send(rsn + " is a regular account")

        blank_stats = Image.open("osrs_stats.png")
        stats_font = ImageFont.truetype('runescape.ttf', 20)
        stats_edit = ImageDraw.Draw(blank_stats)

        stats_edit.text((40,15), str(main_stats.skill('attack', 'level')), (255, 255, 0), font=stats_font)
        stats_edit.text((103,15), str(main_stats.skill('hitpoints', 'level')), (255, 255, 0), font=stats_font)
        stats_edit.text((168,15), str(main_stats.skill('mining', 'level')), (255, 255, 0), font=stats_font)

        stats_edit.text((40,48), str(main_stats.skill('strength', 'level')), (255, 255, 0), font=stats_font)
        stats_edit.text((103,48), str(main_stats.skill('agility', 'level')), (255, 255, 0), font=stats_font)
        stats_edit.text((168,48), str(main_stats.skill('smithing', 'level')), (255, 255, 0), font=stats_font)

        stats_edit.text((40,80), str(main_stats.skill('defense', 'level')), (255, 255, 0), font=stats_font)
        stats_edit.text((103,80), str(main_stats.skill('herblore', 'level')), (255, 255, 0), font=stats_font)
        stats_edit.text((168,80), str(main_stats.skill('mining', 'level')), (255, 255, 0), font=stats_font)

        stats_edit.text((40,110), str(main_stats.skill('ranged', 'level')), (255, 255, 0), font=stats_font)
        stats_edit.text((103,110), str(main_stats.skill('thieving', 'level')), (255, 255, 0), font=stats_font)
        stats_edit.text((168,110), str(main_stats.skill('cooking', 'level')), (255, 255, 0), font=stats_font)

        stats_edit.text((40,143), str(main_stats.skill('prayer', 'level')), (255, 255, 0), font=stats_font)
        stats_edit.text((103,143), str(main_stats.skill('crafting', 'level')), (255, 255, 0), font=stats_font)
        stats_edit.text((168,143), str(main_stats.skill('firemaking', 'level')), (255, 255, 0), font=stats_font)

        stats_edit.text((40,175), str(main_stats.skill('magic', 'level')), (255, 255, 0), font=stats_font)
        stats_edit.text((103,175), str(main_stats.skill('fletching', 'level')), (255, 255, 0), font=stats_font)
        stats_edit.text((168,175), str(main_stats.skill('woodcutting', 'level')), (255, 255, 0), font=stats_font)

        stats_edit.text((40,207), str(main_stats.skill('runecrafting', 'level')), (255, 255, 0), font=stats_font)
        stats_edit.text((103,207), str(main_stats.skill('slayer', 'level')), (255, 255, 0), font=stats_font)
        stats_edit.text((168,207), str(main_stats.skill('farming', 'level')), (255, 255, 0), font=stats_font)
        
        stats_edit.text((40,240), str(main_stats.skill('construction', 'level')), (255, 255, 0), font=stats_font)
        stats_edit.text((103,240), str(main_stats.skill('hunter', 'level')), (255, 255, 0), font=stats_font)
        stats_edit.text((150,240), str(main_stats.skill('total', 'level')), (255, 255, 0), font=stats_font)

        blank_stats.save("stats_edit.png")

        await ctx.send(file=discord.File('stats_edit.png'))

@stats.error
async def stats(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide RSN")

client.run(os.getenv('TOKEN'))

