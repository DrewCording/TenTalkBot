#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from OSRSBytes import Hiscores
import asyncio
from datetime import datetime
from datetime import date

load_dotenv()
client = commands.Bot(command_prefix='!')

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
sheetclient = gspread.authorize(creds)

@client.event
async def on_ready():
    print('!givefriend started on bot {0.user}'.format(client))


@client.command()
@commands.has_permissions(manage_roles=True)
async def givefriend(ctx, user: discord.Member, rsn):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    await ctx.send("Checking rank status...")
    
    ranked=0
    rsn = str(rsn)
    rsn_nospace = rsn.replace(" ","%20")
    sheet_frnd = sheetclient.open_by_key(os.getenv('sheet')).worksheet("Clan Friends")
    sheet_smry = sheetclient.open_by_key(os.getenv('sheet')).worksheet("Member Summary")
    sheet_stat = sheetclient.open_by_key(os.getenv('sheet')).worksheet("Member Stats")

    brnze_role = discord.utils.get(ctx.guild.roles, name="Bronze")
    nana3_role = discord.utils.get(ctx.guild.roles, name="🍌🍌🍌")
    nana2_role = discord.utils.get(ctx.guild.roles, name="🍌🍌")
    nana1_role = discord.utils.get(ctx.guild.roles, name="🍌")
    aplct_role = discord.utils.get(ctx.guild.roles, name="Applicant")
    frend_role = discord.utils.get(ctx.guild.roles, name="Clan Friend")
    leadr_role = discord.utils.get(ctx.guild.roles, name="Leader")
    concl_role = discord.utils.get(ctx.guild.roles, name="Council")

    if brnze_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is a clan member. Demoting them to friend. Use !giverank to undo this.")
        await user.remove_roles(brnze_role)
        ranked=1
    
    elif nana3_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is a clan member. Demoting them to friend. Use !giverank to undo this.")
        await user.remove_roles(nana3_role)
        ranked=1

    elif nana2_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is a clan member. Demoting them to friend. Use !giverank to undo this.")
        await user.remove_roles(nana2_role)
        ranked=1
    
    elif nana1_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is a clan member. Demoting them to friend. Use !giverank to undo this.")
        await user.remove_roles(nana1_role)
        ranked=1

    elif aplct_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is a clan member. Demoting them to friend. Use !giverank to undo this.")
        await user.remove_roles(aplct_role)
        ranked=1

    elif frend_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is already a Clan Friend.")
        return

    elif leadr_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is a clan Leader, cannot demote them to friend.")
        return

    elif concl_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is on clan Council, cannot demote them to friend.")
        return
    
    try:
        main_stats = Hiscores(rsn_nospace, 'N')
    except:
        await ctx.send("RSN " + rsn + " not found on hiscores. Must provide vaild RSN to give friend.")
        main_stats = 0
        return

    i=0
    for membername in sheet_frnd.col_values(1):
        i=i+1
        if str(membername) == str(user):
            await ctx.send("<@!" + str(user.id) + "> (RSN " + sheet_frnd.cell(i, 2).value + ") is already in the clan friend list, but not ranked friend in Discord?")
            await ctx.send("Please manually correct this <@!" + str(ctx.author.id) + ">")
            return
    
    i=0
    for memberrsn in sheet_frnd.col_values(2):
        i=i+1
        if str(memberrsn) == str(rsn):
            await ctx.send("RSN " + rsn + " (@" + sheet_frnd.cell(i, 1).value +  ") is already in the clan friend list, did their Discord name change?")
            await ctx.send("Please manually correct this <@!" + str(ctx.author.id) + ">")
            return

    new_frnd = [str(user), str(rsn)]

    new_frnd.append(str(""))
    new_frnd.append(str("Clan Friend"))
    new_frnd.append(str("=COUNTIF(Offences!A1:A,B" + str(i) + ")+COUNTIF(Offences!A1:A,A" + str(i) + ")"))
    new_frnd.append(str(user.joined_at))
    new_frnd.append(str(""))

    sheet_frnd.append_row(new_frnd, "USER_ENTERED")

    await user.add_roles(frend_role)
    await ctx.send("You must also manually assign this rank ingame, <@!" + str(ctx.author.id) + ">")

    if ranked:
        i=0
        for membername in sheet_smry.col_values(1):
            i=i+1
            if str(membername) == str(user):
                sheet_smry.delete_rows(i)
                sheet_stat.delete_rows(i)

    print(datetime.now())
    print(str(str(ctx.author) + " gave friend to " + str(user) + " with RSN " + rsn))
    await user.edit(nick=rsn)

@givefriend.error
async def givefriend_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage roles to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !givefriend without permission")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide @DiscordUser and RSN")
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("Invalid Discord User")

client.run(os.getenv('TOKEN'))
