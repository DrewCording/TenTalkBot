#!/bin/python3
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from OSRSBytes import Hiscores

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!rankup started on bot {0.user}'.format(client))

@client.command()
@commands.has_permissions(manage_roles=True)
async def stats(ctx, rsn):
    rsn_nospace = rsn.replace(" ","%20")
    await ctx.send("Looking up stats for RSN " + str(rsn))
    try: 
        main_stats = Hiscores(rsn_nospace, 'N')
    except: 
        await ctx.send("RSN " + rsn + " not found on highscores")
        main_stats = 0

    if main_stats:
        try: 
            iron_stats = Hiscores(rsn_nospace, 'IM')
        except:
            iron_stats = 0

        if iron_stats:
            await ctx.send(rsn + " is an ironman")
            await ctx.send("Total level is " + iron_stats.skill('total', 'level'))
        else:
            await ctx.send(rsn + " is a regular account")
            await ctx.send("Total Level is " + main_stats.skill('total', 'level'))
    
    
'''
@stats.error
async def stats(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("User does not exist")
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide @User")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage roles to run this command")
'''
client.run(os.getenv('TOKEN'))

