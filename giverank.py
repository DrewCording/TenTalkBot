#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from OSRSBytes import Hiscores

load_dotenv()
client = commands.Bot(command_prefix='!')

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
sheetclient = gspread.authorize(creds)

@client.event
async def on_ready():
    print('!giverank started on bot {0.user}'.format(client))


@client.command()
@commands.has_permissions(manage_roles=True)
async def giverank(ctx, user: discord.Member, rsn):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    rsn_nospace = rsn.replace(" ","%20")
    await ctx.send('Giving Rank')
    sheet = sheetclient.open_by_key(os.getenv('sheet')).worksheet("Member Summary")
    
    i=0
    for membername in sheet.col_values(1):
        i=i+1
        if str(membername) == str(user):
            print("Found user ", membername, " on row ", i)
            sheet.update_cell(i, 12, "Should be banned")
            
    
'''
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
            try:
                uim_stats = Hiscores(rsn_nospace, 'UIM')
            except: 
                uim_stats = 0

            if uim_stats: 
                await ctx.send(rsn + " is a UIM")
                await ctx.send("Total level is " + uim_stats.skill('total', 'level'))
             else:
                await ctx.send(rsn + " is an Ironman")
                await ctx.send("Total level is " + iron_stats.skill('total', 'level'))
        else:
            await ctx.send(rsn + " is a regular account")
            await ctx.send("Total Level is " + main_stats.skill('total', 'level'))
'''

client.run(os.getenv('TOKEN'))
