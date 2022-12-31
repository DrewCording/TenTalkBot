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
import matplotlib.pyplot as plt
import numpy as np
import time
import re
from discord.utils import get
import random
import twitch
from OSRSBytes import Hiscores
from PIL import Image, ImageFont, ImageDraw

load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)

helix = twitch.Helix(os.getenv('twitch_client'), os.getenv('twitch_secret'))

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
sheetclient = gspread.authorize(creds)

@client.event
async def on_ready():
    print('super bot started on bot {0.user}'.format(client))

@client.command()
async def online(ctx):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    online_file = open("cc_online.log", "r")

    online_users = ""
    for rsn in online_file:
        online_users = str(online_users + rsn.strip() + ", ")

    if online_users:
        await ctx.channel.send("Currently online in CC: ")
        await ctx.channel.send(online_users)
    else:
        await ctx.channel.send("No users currently online in CC")

@client.listen()
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!hello":
        if message.author == client.user:
            if message.channel.id == int(os.getenv('botchan')):
                cc_chan = client.get_channel(int(os.getenv('channel')))
                await cc_chan.send('*Hello!')
        else:
            await message.channel.send('Hello!')
    else:
        return

@client.listen()
async def on_message(message):
    if message.author == client.user:
        if message.channel.id == int(os.getenv('channel')):
            content = str(message.content)
            flag=0
            user_ptrn = "@(.*?)@"
            chan_ptrn = "#(.*?)#"
            levl_ptrn = "] : (.*?) has reached"
            drop_ptrn = "] : (.*?) received a drop"
            qwst_ptrn = "] : (.*?) has completed a quest"
            pets_ptrn = "] : (.*?) has a funny feeling like"
            pkrs_ptrn = "] : (.*?) has been defeated by"
            user_ment = re.search(user_ptrn, content)
            chan_ment = re.search(chan_ptrn, content)
            levl_ment = re.search(levl_ptrn, content)
            drop_ment = re.search(drop_ptrn, content)
            qwst_ment = re.search(qwst_ptrn, content)
            pets_ment = re.search(pets_ptrn, content)
            pkrs_ment = re.search(pkrs_ptrn, content)

            if user_ment:
                user_name = user_ment.group(1)

                for member in message.guild.members:
                    user_full = str("@" + user_name + "@")
                    name = member.name
                    if member.nick:
                        nick = member.nick
                        if nick.lower() == user_name.lower():
                            content = content.replace(user_full, str('<@' + str(member.id) + '>'))
                            flag=1
                            break
                    if name.lower() == user_name.lower():
                        content = content.replace(user_full, str('<@' + str(member.id) + '>'))
                        flag=1
                        break

            if chan_ment:
                chan_name = chan_ment.group(1)

                for channel in message.guild.channels:
                    chan_full = str("#" + chan_name + "#")
                    name = channel.name

                    if name.lower() == chan_name.lower():
                        content = content.replace(chan_full, str('<#' + str(channel.id) + '>'))
                        flag = 1
                        break

            cmd_cfg = open("ccbot_commands.cfg", "r")
            bot_chan = client.get_channel(int(os.getenv('botchan')))

            for cmd in cmd_cfg:
                content_l = content.lower()
                cmd_ment = content_l.find(str("!" + cmd.strip()))

                if cmd_ment > 0:
                    await bot_chan.send(str("!" + cmd.strip()))

            cmd_cfg.close()

            if flag:
                await message.channel.send(content)
                await message.delete()
            else:
                if levl_ment:
                    levl_name = levl_ment.group(1)
                    await message.channel.send("*Gz @" + levl_name + " on the level")
                elif drop_ment:
                    drop_name = drop_ment.group(1)
                    await message.channel.send("*Gz @" + drop_name + " on the drop")
                elif qwst_ment:
                    qwst_name = qwst_ment.group(1)
                    await message.channel.send("*Gz @" + qwst_name + " on the quest")
                elif pets_ment:
                    pets_name = pets_ment.group(1)
                    await message.channel.send("*Gz @" + pets_name + " on the pet")
                elif pkrs_ment:
                    pkrs_name = pkrs_ment.group(1)
                    await message.channel.send("*lmao sit @" + pkrs_name)


    else:
        return

@client.listen()
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        if message.author == client.user:
            content = str(message.content)
            if content.startswith('*'):
                return

            rsn_ptrn = "] (.*?): "
            login_ptrn = "0>(.*?) has joined"
            logot_ptrn = "0>(.*?) has left"
            emt_ptrn = "<:(.*?)>"

            rsn = re.search(rsn_ptrn, content)
            login = re.search(login_ptrn, content)
            logot = re.search(logot_ptrn, content)
            emt = re.search(emt_ptrn, content)

            if login:
                cc_logins = open("cc_logins.log", "a")
                cc_logins.write(str(str(login.group(1)) + "\n"))
                cc_logins.close()

                cc_online = open("cc_online.log", "a")
                cc_online.write(str(str(login.group(1)) + "\n"))
                cc_online.close()

                await asyncio.sleep(15)
                await message.delete()

            if logot:
                cc_online = open("cc_online.log", "r")
                cc_online_content = cc_online.readlines()
                cc_online.close()

                cc_online = open("cc_online.log", "w")
                for logout_rsn in cc_online_content:
                    if logout_rsn.strip() != logot.group(1):
                        cc_online.write(logout_rsn)
                cc_online.close()

                await asyncio.sleep(15)
                await message.delete()

            if rsn:
                if emt:
                    emt_full = str("<:" + str(emt.group(1)) + ">")
                    rsn = str(rsn.group(1)).replace(emt_full, "")
                else:
                    rsn = rsn.group(1)

                cc_messages = open("cc_messages.log", "a")
                cc_messages.write(str(rsn + "\n"))
                cc_messages.close()

        else:
            print(message.author,":",message.content)
    else:
        return

@client.listen()
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!commands":
        if message.author == client.user:
            if message.channel.id == int(os.getenv('botchan')):
                cc_chan = client.get_channel(int(os.getenv('channel')))

                cmd_cfg = open("ccbot_commands.cfg", "r")
                cmdlist = "Prefix !: "
                for cmd in cmd_cfg:
                    cmdlist = str(cmdlist + cmd.strip() + ", ")

                cmd_cfg.close()
                await cc_chan.send(str("*" + cmdlist))

        else:
            cmd_cfg = open("disc_commands.cfg", "r")
            cmdlist = ""
            for cmd in cmd_cfg:
                cmdlist = str(cmdlist + "!" + cmd.strip() + ", ")

            cmd_cfg.close()
            await message.channel.send(cmdlist)
    else:
        return

@client.listen()
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!discord":
            if message.author == client.user:
                if message.channel.id == int(os.getenv('botchan')):
                    cc_chan = client.get_channel(int(os.getenv('channel')))
                    #await cc_chan.send('*Head to www tentalkosrs com for a Discord invite')
                    await cc_chan.send('*Head to tentalk.ca for a Discord invite')
            else:
                #await message.channel.send('Head to https://www.tentalkosrs.com for a Discord invite')
                await message.channel.send('Head to tentalk.ca for a Discord invite')

    else:
        return

@client.command()
@commands.has_permissions(manage_roles=True)
async def givefriend(ctx, user: discord.Member, rsn):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    if ctx.channel.category_id != int(os.getenv('app_cat')):
        await ctx.send("This command can only be used in an application channel")
        return

    await ctx.send("Checking rank status...")

    ranked=0
    rsn = str(rsn)
    rsn_nospace = rsn.replace(" ","%20")
    sheet_frnd = sheetclient.open_by_key(os.getenv('sheet')).worksheet("Clan Friends")
    sheet_smry = sheetclient.open_by_key(os.getenv('sheet')).worksheet("Member Summary")
    sheet_stat = sheetclient.open_by_key(os.getenv('sheet')).worksheet("Member Stats")

    memb_role = discord.utils.get(ctx.guild.roles, name="Clan Member")
    rune_role = discord.utils.get(ctx.guild.roles, name="Rune")
    addy_role = discord.utils.get(ctx.guild.roles, name="Addy")
    mith_role = discord.utils.get(ctx.guild.roles, name="Mith")
    stel_role = discord.utils.get(ctx.guild.roles, name="Steel")
    iron_role = discord.utils.get(ctx.guild.roles, name="Iron")
    brnz_role = discord.utils.get(ctx.guild.roles, name="Bronze")
    maxd_role = discord.utils.get(ctx.guild.roles, name="Maxed")
    frend_role = discord.utils.get(ctx.guild.roles, name="Clan Friend")
    leadr_role = discord.utils.get(ctx.guild.roles, name="Leader")
    concl_role = discord.utils.get(ctx.guild.roles, name="Council")
    unverified = discord.utils.get(ctx.guild.roles, name="unverified")

    if memb_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is a clan member. Demoting them to friend. Use !giverank to undo this.")
        await user.remove_roles(memb_role)
        await user.remove_roles(rune_role)
        await user.remove_roles(addy_role)
        await user.remove_roles(mith_role)
        await user.remove_roles(stel_role)
        await user.remove_roles(iron_role)
        await user.remove_roles(brnz_role)
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
    await user.remove_roles(unverified)
    await ctx.send("Gave Clan Friend rank to <@!" + str(user.id) + ">")
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

    await ctx.send("This channel will self-destruct in 24 hours")
    await asyncio.sleep(86400)
    await ctx.channel.delete()
 

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

@client.command()
@commands.has_permissions(manage_roles=True)
async def giverank(ctx, user: discord.Member, rsn):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    if ctx.channel.category_id != int(os.getenv('app_cat')):
        await ctx.send("This command can only be used in an application channel")
        return

    await ctx.send("Checking rank status...")

    friend=0
    rsn = str(rsn)
    rsn_nospace = rsn.replace(" ","%20")
    sheet_frnd = sheetclient.open_by_key(os.getenv('sheet')).worksheet("Clan Friends")
    sheet_smry = sheetclient.open_by_key(os.getenv('sheet')).worksheet("Member Summary")
    sheet_stat = sheetclient.open_by_key(os.getenv('sheet')).worksheet("Member Stats")

    memb_role = discord.utils.get(ctx.guild.roles, name="Clan Member")
    rune_role = discord.utils.get(ctx.guild.roles, name="Rune")
    addy_role = discord.utils.get(ctx.guild.roles, name="Addy")
    mith_role = discord.utils.get(ctx.guild.roles, name="Mith")
    stel_role = discord.utils.get(ctx.guild.roles, name="Steel")
    iron_role = discord.utils.get(ctx.guild.roles, name="Iron")
    brnz_role = discord.utils.get(ctx.guild.roles, name="Bronze")
    maxd_role = discord.utils.get(ctx.guild.roles, name="Maxed")
    frend_role = discord.utils.get(ctx.guild.roles, name="Clan Friend")
    leadr_role = discord.utils.get(ctx.guild.roles, name="Leader")
    concl_role = discord.utils.get(ctx.guild.roles, name="Council")
    unverified = discord.utils.get(ctx.guild.roles, name="unverified")

    if memb_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is already ranked in clan. Use !rankup to change.")
        return

    elif frend_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is currently a clan friend. Giving them full Clan membership (if 10HP).")
        friend=1

    elif leadr_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is a clan Leader, cannot give them member rank.")
        return

    elif concl_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is on clan Council, cannot give them member rank.")
        return

    try:
        main_stats = Hiscores(rsn_nospace, 'N')
    except:
        await ctx.send("RSN " + rsn + " not found on hiscores. Must provide vaild RSN to give rank.")
        main_stats = 0
        return

    i=0
    for membername in sheet_smry.col_values(1):
        i=i+1
        if str(membername) == str(user):
            await ctx.send("<@!" + str(user.id) + "> (RSN " + sheet_smry.cell(i, 2).value + ") is already in the clan member list, but not ranked in Discord? They should be ranked " + sheet_smry.cell(i, 8).value)
            await ctx.send("Please manually correct this <@!" + str(ctx.author.id) + ">")
            return

    i=0
    for memberrsn in sheet_smry.col_values(2):
        i=i+1
        if str(memberrsn) == str(rsn):
            await ctx.send("RSN " + rsn + " (@" + sheet_smry.cell(i, 1).value +  ") is already in the clan member list, did their Discord name change? They should be ranked " + sheet_smry.cell(i, 8).value)
            await ctx.send("Please manually correct this <@!" + str(ctx.author.id) + ">")
            return
    i=i+1

    new_stats = [str(user), str(rsn)]
    new_smry = [str("='Member Stats'!A" + str(i)), str("='Member Stats'!B" + str(i))]

    if main_stats:
        try:
            iron_stats = Hiscores(rsn_nospace, 'IM')
        except:
            iron_stats = 0

        if iron_stats:
            new_stats.append(int(iron_stats.skill('total', 'level')))

            try:
                uim_stats = Hiscores(rsn_nospace, 'UIM')
            except:
                uim_stats = 0

            if uim_stats:
                new_stats.append(int(uim_stats.skill('total', 'level')))
                new_stats.append('N/A')
            else:
                try:
                    hci_stats = Hiscores(rsn_nospace, 'HIM')
                except:
                    hci_stats = 0

                if hci_stats:
                    new_stats.append('N/A')
                    new_stats.append(int(hci_stats.skill('total', 'level')))
                else:
                    new_stats.append('N/A')
                    new_stats.append('N/A')

        else:
            new_stats.append('N/A')
            new_stats.append('N/A')
            new_stats.append('N/A')

    new_stats.append(int(main_stats.skill('total', 'level')))
    new_stats.append(int(main_stats.skill('attack', 'level')))
    new_stats.append(int(main_stats.skill('defense', 'level')))
    new_stats.append(int(main_stats.skill('strength', 'level')))
    new_stats.append(int(main_stats.skill('hitpoints', 'level')))
    new_stats.append(int(main_stats.skill('ranged', 'level')))
    new_stats.append(int(main_stats.skill('prayer', 'level')))
    new_stats.append(int(main_stats.skill('magic', 'level')))
    new_stats.append(int(main_stats.skill('cooking', 'level')))
    new_stats.append(int(main_stats.skill('woodcutting', 'level')))
    new_stats.append(int(main_stats.skill('fletching', 'level')))
    new_stats.append(int(main_stats.skill('fishing', 'level')))
    new_stats.append(int(main_stats.skill('firemaking', 'level')))
    new_stats.append(int(main_stats.skill('crafting', 'level')))
    new_stats.append(int(main_stats.skill('smithing', 'level')))
    new_stats.append(int(main_stats.skill('mining', 'level')))
    new_stats.append(int(main_stats.skill('herblore', 'level')))
    new_stats.append(int(main_stats.skill('agility', 'level')))
    new_stats.append(int(main_stats.skill('thieving', 'level')))
    new_stats.append(int(main_stats.skill('slayer', 'level')))
    new_stats.append(int(main_stats.skill('farming', 'level')))
    new_stats.append(int(main_stats.skill('runecrafting', 'level')))
    new_stats.append(int(main_stats.skill('hunter', 'level')))
    new_stats.append(int(main_stats.skill('construction', 'level')))


    new_smry.append(str("=MAX('Member Stats'!C" + str(i) + ", 'Member Stats'!D" + str(i) + ",'Member Stats'!E" + str(i) + ",'Member Stats'!F" + str(i) + ")"))
    new_smry.append(str("=0.25*('Member Stats'!H" + str(i) + "+'Member Stats'!J" + str(i) + "+0.5*'Member Stats'!L" + str(i) + ")+MAX((13/40)*('Member Stats'!I" + str(i) + "+'Member Stats'!G" + str(i) + "),((13/40)*('Member Stats'!K" + str(i) + "*1.5)),((13/40)*('Member Stats'!M" + str(i) + "*1.5)))"))
    new_smry.append("='Member Stats'!J" + str(i))
    new_smry.append(str("=COUNTIF('Member Stats'!G" + str(i) + ":M" + str(i) + ",\">10\")"))
    new_smry.append(str("=IF(ISNUMBER('Member Stats'!C" + str(i) + "),IF(ISNUMBER('Member Stats'!D" + str(i) + "),\"UIM\",IF(ISNUMBER('Member Stats'!E" + str(i) + "),IF('Member Stats'!C" + str(i) + " > 'Member Stats'!E" + str(i) + ",\"Dead HCIM\",\"HCIM\"),\"IM\")),\"Normal\")"))
    new_smry.append(str("=IF(E" + str(i) + ">10,\"Clan Friend\",(IF(G" + str(i) + "=\"Normal\",(IF(F" + str(i) + "<1,(IF(C" + str(i) + ">=1500,\"Rune\",(IF(C" + str(i) + ">=1400,\"Adamant\",(IF(C" + str(i) + ">=1200,\"Mithril\",(IF(C" + str(i) + ">=900,\"Steel\",(IF(C" + str(i) + ">=600,\"Iron\",\"Bronze\")))))))))),(IF(F" + str(i) + "<3,(IF(C" + str(i) + ">=1666,\"Rune\",(IF(C" + str(i) + ">=1533,\"Adamant\",(IF(C" + str(i) + ">=1300,\"Mithril\",(IF(C" + str(i) + ">=966,\"Steel\",(IF(C" + str(i) + ">=633,\"Iron\",\"Bronze\")))))))))),(IF(F" + str(i) + "<5,(IF(C" + str(i) + ">=1833,\"Rune\",(IF(C" + str(i) + ">=1666,\"Adamant\",(IF(C" + str(i) + ">=1400,\"Mithril\",(IF(C" + str(i) + ">=1033,\"Steel\",(IF(C" + str(i) + ">=666,\"Iron\",\"Bronze\")))))))))),(IF(C" + str(i) + ">=2000,\"Rune\",(IF(C" + str(i) + ">=1800,\"Adamant\",(IF(C" + str(i) + ">=1500,\"Mithril\",(IF(C" + str(i) + ">=1100,\"Steel\",(IF(C" + str(i) + ">=700,\"Iron\",\"Bronze\")))))))))))))))),(IF(OR(G" + str(i) + "=\"IM\",G" + str(i) + "=\"Dead HCIM\",G" + str(i) + "=\"HCIM\"),(IF(F" + str(i) + "<1,(IF(C" + str(i) + ">=1500,\"Rune\",(IF(C" + str(i) + ">=1300,\"Adamant\",(IF(C" + str(i) + ">=1100,\"Mithril\",(IF(C" + str(i) + ">=800,\"Steel\",(IF(C" + str(i) + ">=500,\"Iron\",\"Bronze\")))))))))),(IF(F" + str(i) + "<3,(IF(C" + str(i) + ">=1666,\"Rune\",(IF(C" + str(i) + ">=1433,\"Adamant\",(IF(C" + str(i) + ">=1200,\"Mithril\",(IF(C" + str(i) + ">=866,\"Steel\",(IF(C" + str(i) + ">=533,\"Iron\",\"Bronze\")))))))))),(IF(F" + str(i) + "<5,(IF(C" + str(i) + ">=1833,\"Rune\",(IF(C" + str(i) + ">=1566,\"Adamant\",(IF(C" + str(i) + ">=1300,\"Mithril\",(IF(C" + str(i) + ">=933,\"Steel\",(IF(C" + str(i) + ">=566,\"Iron\",\"Bronze\")))))))))),(IF(C" + str(i) + ">=2000,\"Rune\",(IF(C" + str(i) + ">=1700,\"Adamant\",(IF(C" + str(i) + ">=1400,\"Mithril\",(IF(C" + str(i) + ">=1000,\"Steel\",(IF(C" + str(i) + ">=600,\"Iron\",\"Bronze\")))))))))))))))),(IF(G" + str(i) + "=\"UIM\",(IF(F" + str(i) + "<1,(IF(C" + str(i) + ">=1500,\"Rune\",(IF(C" + str(i) + ">=1200,\"Adamant\",(IF(C" + str(i) + ">=1000,\"Mithril\",(IF(C" + str(i) + ">=700,\"Steel\",(IF(C" + str(i) + ">=400,\"Iron\",\"Bronze\")))))))))),(IF(F" + str(i) + "<3,(IF(C" + str(i) + ">=1666,\"Rune\",(IF(C" + str(i) + ">=1333,\"Adamant\",(IF(C" + str(i) + ">=1100,\"Mithril\",(IF(C" + str(i) + ">=766,\"Steel\",(IF(C" + str(i) + ">=433,\"Iron\",\"Bronze\")))))))))),(IF(F" + str(i) + "<5,(IF(C" + str(i) + ">=1833,\"Rune\",(IF(C" + str(i) + ">=1466,\"Adamant\",(IF(C" + str(i) + ">=1200,\"Mithril\",(IF(C" + str(i) + ">=833,\"Steel\",(IF(C" + str(i) + ">=466,\"Iron\",\"Bronze\")))))))))),(IF(C" + str(i) + ">=2000,\"Rune\",(IF(C" + str(i) + ">=1600,\"Adamant\",(IF(C" + str(i) + ">=1300,\"Mithril\",(IF(C" + str(i) + ">=900,\"Steel\",(IF(C" + str(i) + ">=500,\"Iron\",\"Bronze\")))))))))))))))),\"ERROR\")))))))"))
    new_smry.append(str(""))
    new_smry.append(str(""))
    new_smry.append(str("=COUNTIF(Offences!A1:A,B" + str(i) + ")+COUNTIF(Offences!A1:A,A" + str(i) + ")"))
    new_smry.append(str(user.joined_at))
    new_smry.append(str(""))

    sheet_stat.append_row(new_stats, "USER_ENTERED")
    sheet_smry.append_row(new_smry, "USER_ENTERED")

    await asyncio.sleep(1)
    recom_rank = sheet_smry.cell(i, 8).value

    if friend:
        await user.remove_roles(frend_role)
        j=0
        for membername in sheet_frnd.col_values(1):
            j=j+1
            if str(membername) == str(user):
                sheet_frnd.delete_rows(j)

    if str(recom_rank) == "Clan Friend":
        await ctx.send(rsn + " is not 10HP, giving Clan Friend rank to <@!" + str(user.id) + ">")
        await ctx.send("You can manually override this if desired to admit the member anyway")
        await user.add_roles(frend_role)
        sheet_smry.update_cell(i, 10, "Clan Friend")

    elif str(recom_rank) == "Bronze":
        await ctx.send(rsn + " is " + str(sheet_smry.cell(i, 3).value) + " total, giving Bronze rank to <@!" + str(user.id) + ">")
        await user.add_roles(brnz_role)
        sheet_smry.update_cell(i, 10, "Bronze")

    elif str(recom_rank) == "Iron":
        await ctx.send(rsn + " is " + str(sheet_smry.cell(i, 3).value)  + " total, giving Iron rank to <@!" + str(user.id) + ">")
        await user.add_roles(iron_role)
        sheet_smry.update_cell(i, 10, "Iron")

    elif str(recom_rank) == "Steel":
        await ctx.send(rsn + " is " + str(sheet_smry.cell(i, 3).value)  + " total, giving Steel rank to <@!" + str(user.id) + ">")
        await user.add_roles(stel_role)
        sheet_smry.update_cell(i, 10, "Steel")

    elif str(recom_rank) == "Mithril":
        await ctx.send(rsn + " is " + str(sheet_smry.cell(i, 3).value)  + " total, giving Mith rank to <@!" + str(user.id) + ">")
        await user.add_roles(mith_role)
        sheet_smry.update_cell(i, 10, "Mithril")

    elif str(recom_rank) == "Adamant":
        await ctx.send(rsn + " is " + str(sheet_smry.cell(i, 3).value)  + " total, giving Addy rank to <@!" + str(user.id) + ">")
        await user.add_roles(addy_role)
        sheet_smry.update_cell(i, 10, "Adamant")

    elif str(recom_rank) == "Rune":
        await ctx.send(rsn + " is " + str(sheet_smry.cell(i, 3).value)  + " total, giving Rune rank to <@!" + str(user.id) + ">")
        await user.add_roles(rune_role)
        sheet_smry.update_cell(i, 10, "Rune")


    await user.add_roles(memb_role)
    await user.remove_roles(unverified)
    await user.edit(nick=rsn)
    await ctx.send("You must also manually assign this rank ingame, <@!" + str(ctx.author.id) + ">")

    print(datetime.now())
    print(str(str(ctx.author) + " gave rank to " + str(user) + " with RSN " + rsn))

    await ctx.send("This channel will self-destruct in 24 hours")
    await asyncio.sleep(86400)
    await ctx.channel.delete()

@giverank.error
async def giverank_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage roles to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !giverank without permission")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide @DiscordUser and RSN")
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("Invalid Discord User")

@client.listen()
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!info":
        if message.author == client.user:
            if message.channel.id == int(os.getenv('botchan')):
                try:
                    info_file = open("info_cc.msg", "r")
                    info_msg = info_file.read()
                    info_file.close()
                except:
                    info_msg = "No info message is set"

                cc_chan = client.get_channel(int(os.getenv('channel')))
                await cc_chan.send(str('*' + info_msg))
        else:
            try:
                info_file = open("info_disc.msg", "r")
                info_msg = info_file.read()
                info_file.close()
            except:
                info_msg = "No info message is set"

            await message.channel.send(str(info_msg))
    else:
        return

@client.command()
@commands.has_permissions(manage_messages=True)
async def info_set(ctx, typ, info):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    if typ.lower() == "discord":
        info_file = open("info_disc.msg", "w")
        info_file.write(str(info))
        info_file.close()
        await ctx.send("Info Discord message set to:")
        info_file = open("info_disc.msg", "r")
        await ctx.send(str(info_file.read()))
        print(ctx.author, "set Discord info message to", info)
        info_file.close()

    elif typ.lower() == "cc":
        if len(info) > 79:
            await ctx.send("Message too long. Character limit is 79 for info cc message")
            await ctx.send(str("Your message is " + str(len(info)) + " characters"))
        else:
            info_file = open("info_cc.msg", "w")
            info_file.write(str(info))
            info_file.close()
            await ctx.send("Info CC message set to:")
            info_file = open("info_cc.msg", "r")
            await ctx.send(str(info_file.read()))
            print(ctx.author, "set CC info message to", info)
            info_file.close()

    else:
        await ctx.send("Info type not valid. Specify either 'cc' or 'discord'")

@info_set.error
async def info_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide a message to set")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage messages to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !info_set without permission")

@client.listen()
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!motd":
        if message.author == client.user:
            if message.channel.id == int(os.getenv('botchan')):
                try:
                    motd_file = open("motd_cc.msg", "r")
                    motd_msg = motd_file.read()
                    motd_file.close()
                except:
                    motd_msg = "No motd is set"

                cc_chan = client.get_channel(int(os.getenv('channel')))
                await cc_chan.send(str('*' + motd_msg))
        else:
            try:
                motd_file = open("motd_disc.msg", "r")
                motd_msg = motd_file.read()
                motd_file.close()
            except:
                motd_msg = "No motd is set"

            await message.channel.send(str(motd_msg))
    else:
        return

@client.command()
@commands.has_permissions(manage_messages=True)
async def motd_set(ctx, typ, motd):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    if typ.lower() == "discord":
        motd_file = open("motd_disc.msg", "w")
        motd_file.write(str(motd))
        motd_file.close()
        await ctx.send("MOTD Discord message set to:")
        motd_file = open("motd_disc.msg", "r")
        await ctx.send(str(motd_file.read()))
        print(ctx.author, "set the Discord motd to", motd)
        motd_file.close()

    elif typ.lower() == "cc":
        if len(motd) > 79:
            await ctx.send("Message too long. Character limit is 79 for motd cc message")
            await ctx.send(str("Your message is " + str(len(motd)) + " characters"))
        else:
            motd_file = open("motd_cc.msg", "w")
            motd_file.write(str(motd))
            motd_file.close()
            await ctx.send("MOTD CC message set to:")
            motd_file = open("motd_cc.msg", "r")
            await ctx.send(str(motd_file.read()))
            print(ctx.author, "set the CC motd to", motd)
            motd_file.close()

    else:
        await ctx.send("MOTD type not valid. Specify either 'cc' or 'discord'")

@motd_set.error
async def motd_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide a message to set")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage messages to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !motd_set without permission")

@client.command()
#@commands.has_permissions(manage_messages=True)
async def poll_cancel(ctx, poll_num: int):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    if os.path.exists(str("poll" + str(poll_num) + ".tmp")):
        poll_file = open(str("poll" + str(poll_num) + ".tmp"), "r")
        poll_data = poll_file.readlines()
        poll_file.close()

        if str(poll_data[1]).strip() == str(ctx.author.id):
            os.remove(str("poll" + str(poll_num) + ".tmp"))
            await ctx.send("Cancelled poll #" + str(poll_num) + " by <@!" + str(poll_data[1]).strip() + ">")
        elif ctx.author.guild_permissions.manage_messages:
            os.remove(str("poll" + str(poll_num) + ".tmp"))
            await ctx.send("Cancelled poll #" + str(poll_num) + " by <@!" + str(poll_data[1]).strip() + ">")
        else:
            await ctx.send("You can only cancel your own polls without mod status.")
            print(str(str(datetime.now()) + str(ctx.author) + " attempted to delete a poll without permission"))
    else:
        await ctx.send("Poll #" + str(poll_num) + " not currently running")

@poll_cancel.error
async def poll_cancel_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide poll number to cancel")

@client.command()
async def poll(ctx, ttl: int, question: str, *options: str):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    if len(options) == 0:
        await ctx.channel.send("You must provide at least 1 option")
        return

    poll_chan = client.get_channel(int(os.getenv('poll_chan')))

    try:
        polls_hist = open("polls.hist", "r")
        poll_num = len(polls_hist.readlines())
        polls_hist.close()
    except:
        ctx.channel.send("Error in creating poll. Contact Ten Talk Bot Admin")
        return

    poll_msg = str("Poll #" + str(poll_num+1) + ": " + question)

    polls_hist = open("polls.hist", "a")
    polls_hist.write(str(str(datetime.now()) + " " + poll_msg + " by: " + str(ctx.author) + "\n"))
    polls_hist.close()

    poll_msg = str(poll_msg + "\n" + "by: <@!" + str(ctx.author.id) + ">\n")

    if ttl < 60:
        ttl_flt = ttl
        scale = " minutes"
    else:
        ttl_flt = ttl/60
        if ttl_flt < 24:
            scale = " hours"
        else:
            ttl_flt = ttl_flt/24
            scale = " days"

    ttl_flt = round(ttl_flt, 2)
    poll_msg = str(poll_msg + "Time Left: " + str(ttl_flt) + scale  + "\n\n")

    i=0
    for option in options:
        if i==0:
            poll_msg = str(poll_msg + ":regional_indicator_a: ")
            reactions = ['🇦']
        elif i==1:
            poll_msg = str(poll_msg + ":regional_indicator_b: ")
            reactions.append('🇧')
        elif i==2:
            poll_msg = str(poll_msg + ":regional_indicator_c: ")
            reactions.append('🇨')
        elif i==3:
            poll_msg = str(poll_msg + ":regional_indicator_d: ")
            reactions.append('🇩')
        elif i==4:
            poll_msg = str(poll_msg + ":regional_indicator_e: ")
            reactions.append('🇪')
        elif i==5:
            poll_msg = str(poll_msg + ":regional_indicator_f: ")
            reactions.append('🇫')
        elif i==6:
            poll_msg = str(poll_msg + ":regional_indicator_g: ")
            reactions.append('🇬')
        elif i==7:
            poll_msg = str(poll_msg + ":regional_indicator_h: ")
            reactions.append('🇭')
        elif i==8:
            await ctx.author.send("Warning: !poll is limited to 8 options. Your poll has been truncated to this.")
            break

        poll_msg = str(poll_msg + option + "\n")
        i=i+1

    poll_create = await poll_chan.send(poll_msg)

    for reaction in reactions:
        await poll_create.add_reaction(reaction)

    poll_lock = open(str("poll" + str(poll_num+1) + ".tmp"), "w")
    poll_lock.write(str(question + " by: " + str(ctx.author) + "\n" + str(ctx.author.id) + "\n" + str(poll_create.id)))
    poll_lock.close()

    while ttl:
        await asyncio.sleep(60)
        ttl=ttl-1

        if not os.path.exists(str("poll" + str(poll_num+1) + ".tmp")):
            poll_msg = poll_msg.replace(str("Time Left: " + str(ttl_flt) + scale), str("Time Left: Poll Cancelled"))
            await poll_create.edit(content=poll_msg)
            return

        if ttl < 60:
            ttl_flt_new = ttl
            scale_new = " minutes"
        else:
            ttl_flt_new = ttl/60
            if ttl_flt_new < 24:
                scale_new = " hours"
            else:
                ttl_flt_new = ttl_flt_new/24
                scale_new = " days"

        ttl_flt_new = round(ttl_flt_new, 2)
        poll_msg = poll_msg.replace(str("Time Left: " + str(ttl_flt) + scale), str("Time Left: " + str(ttl_flt_new) + scale_new))
        await poll_create.edit(content=poll_msg)

        ttl_flt = ttl_flt_new
        scale = scale_new

    if os.path.exists(str("poll" + str(poll_num+1) + ".tmp")):
        os.remove(str("poll" + str(poll_num+1) + ".tmp"))

    poll_msg = poll_msg.replace(str("Time Left: " + str(ttl_flt) + scale), str("Time Left: Poll Completed"))
    await poll_create.edit(content=poll_msg)

    poll_result = await poll_chan.fetch_message(int(poll_create.id))
    results = []
    for reaction in poll_result.reactions:
        results.append(reaction.count)

    results = results[0 : len(options)]
    plt.pie(results, labels = options)
    plt.savefig(str("poll" + str(poll_num+1) + ".png"))
    plt.clf()
    await poll_chan.send(str("Poll #" + str(poll_num+1) + " Results by: <@!" + str(ctx.author.id) + ">\n**" + question + "**"), file=discord.File(str("poll" + str(poll_num+1) + ".png")))
    os.remove(str("poll" + str(poll_num+1) + ".png"))

@poll.error
async def poll_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Usage: !poll <minutes> <\"Question\"> <\"Option 1\"> ... <\"Option 8\">")
    elif isinstance(error, discord.ext.commands.errors.BadArgument):
        await ctx.send("Usage: !poll <minutes> <\"Question\"> <\"Option 1\"> ... <\"Option 8\">")
    elif isinstance(error, discord.ext.commands.errors.ExpectedClosingQuoteError):
        await ctx.send("Usage: !poll <minutes> <\"Question\"> <\"Option 1\"> ... <\"Option 8\">")
    else:
        await ctx.send("Error in creating poll. Contact Ten Talk Bot Admin")

@client.listen()
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!raids":
        if message.author == client.user:
            if message.channel.id == int(os.getenv('botchan')):
                cc_chan = client.get_channel(int(os.getenv('channel')))
                await cc_chan.send('*Use this in Discord for an invite to Level 3 Raids server. Free masses weekly')
        else:
            if message.author.nick:
                name = message.author.nick
            else:
                name = message.author.name

            await message.channel.send("If you are interested in learning CoX Raids on a Level 3 or 10HP, check out the Level 3 Raids Discord Server. Free mass raids every week. Invite link: https://discord.gg/wVSkAABhdr")
    else:
        return

@client.command()
@commands.has_permissions(manage_roles=True)
async def rankup(ctx, user: discord.Member):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    await ctx.send("Checking rank status...")

    ready=0
    found=0
    sheet_smry = sheetclient.open_by_key(os.getenv('sheet')).worksheet("Member Summary")
    sheet_stat = sheetclient.open_by_key(os.getenv('sheet')).worksheet("Member Stats")

    memb_role = discord.utils.get(ctx.guild.roles, name="Clan Member")
    rune_role = discord.utils.get(ctx.guild.roles, name="Rune")
    addy_role = discord.utils.get(ctx.guild.roles, name="Addy")
    mith_role = discord.utils.get(ctx.guild.roles, name="Mith")
    stel_role = discord.utils.get(ctx.guild.roles, name="Steel")
    iron_role = discord.utils.get(ctx.guild.roles, name="Iron")
    brnz_role = discord.utils.get(ctx.guild.roles, name="Bronze")
    maxd_role = discord.utils.get(ctx.guild.roles, name="Maxed")
    frend_role = discord.utils.get(ctx.guild.roles, name="Clan Friend")
    leadr_role = discord.utils.get(ctx.guild.roles, name="Leader")
    concl_role = discord.utils.get(ctx.guild.roles, name="Council")


    if maxd_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is already Maxed, can't rank-up any further.")
        return

    elif rune_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is already Rune. Maxed rank-ups must be done manually.")
        return

    elif memb_role in user.roles:
        ready=1

    elif frend_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is currently a clan friend. Use !giverank to add them to the member role.")
        return

    elif leadr_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is a clan Leader, cannot give them member rank.")
        return

    elif concl_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is on clan Council, cannot give them member rank.")
        return

    if not ready:
        await ctx.send("<@!" + str(user.id) + "> is not a clan member. Use !giverank to add new members")
        return

    i=0
    for membername in sheet_smry.col_values(1):
        i=i+1
        if str(membername) == str(user):
            found=1
            break

    if not found:
        await ctx.send("<@!" + str(user.id) + "> is not on the member role. Please check and manually correct it <@!" + str(ctx.author.id) + ">")
        return

    rsn = str(sheet_smry.cell(i, 2).value)
    rsn_nospace = rsn.replace(" ","%20")

    try:
        main_stats = Hiscores(rsn_nospace, 'N')
    except:
        await ctx.send("RSN " + rsn + " not found on hiscores. Did it change? Must manually correct it <@!" + str(ctx.author.id) + ">")
        main_stats = 0
        return

    notes = sheet_smry.cell(i, 13).value
    sheet_stat.delete_rows(i)
    sheet_smry.delete_rows(i)
    i = int(sheet_smry.row_count)

    new_stats = [str(user), str(rsn)]
    new_smry = [str("='Member Stats'!A" + str(i)), str("='Member Stats'!B" + str(i))]

    if main_stats:
        try:
            iron_stats = Hiscores(rsn_nospace, 'IM')
        except:
            iron_stats = 0

        if iron_stats:
            new_stats.append(int(iron_stats.skill('total', 'level')))

            try:
                uim_stats = Hiscores(rsn_nospace, 'UIM')
            except:
                uim_stats = 0

            if uim_stats:
                new_stats.append(int(uim_stats.skill('total', 'level')))
                new_stats.append('N/A')
            else:
                try:
                    hci_stats = Hiscores(rsn_nospace, 'HIM')
                except:
                    hci_stats = 0

                if hci_stats:
                    new_stats.append('N/A')
                    new_stats.append(int(hci_stats.skill('total', 'level')))
                else:
                    new_stats.append('N/A')
                    new_stats.append('N/A')

        else:
            new_stats.append('N/A')
            new_stats.append('N/A')
            new_stats.append('N/A')

    new_stats.append(int(main_stats.skill('total', 'level')))
    new_stats.append(int(main_stats.skill('attack', 'level')))
    new_stats.append(int(main_stats.skill('defense', 'level')))
    new_stats.append(int(main_stats.skill('strength', 'level')))
    new_stats.append(int(main_stats.skill('hitpoints', 'level')))
    new_stats.append(int(main_stats.skill('ranged', 'level')))
    new_stats.append(int(main_stats.skill('prayer', 'level')))
    new_stats.append(int(main_stats.skill('magic', 'level')))
    new_stats.append(int(main_stats.skill('cooking', 'level')))
    new_stats.append(int(main_stats.skill('woodcutting', 'level')))
    new_stats.append(int(main_stats.skill('fletching', 'level')))
    new_stats.append(int(main_stats.skill('fishing', 'level')))
    new_stats.append(int(main_stats.skill('firemaking', 'level')))
    new_stats.append(int(main_stats.skill('crafting', 'level')))
    new_stats.append(int(main_stats.skill('smithing', 'level')))
    new_stats.append(int(main_stats.skill('mining', 'level')))
    new_stats.append(int(main_stats.skill('herblore', 'level')))
    new_stats.append(int(main_stats.skill('agility', 'level')))
    new_stats.append(int(main_stats.skill('thieving', 'level')))
    new_stats.append(int(main_stats.skill('slayer', 'level')))
    new_stats.append(int(main_stats.skill('farming', 'level')))
    new_stats.append(int(main_stats.skill('runecrafting', 'level')))
    new_stats.append(int(main_stats.skill('hunter', 'level')))
    new_stats.append(int(main_stats.skill('construction', 'level')))

    new_smry.append(str("=MAX('Member Stats'!C" + str(i) + ", 'Member Stats'!D" + str(i) + ",'Member Stats'!E" + str(i) + ",'Member Stats'!F" + str(i) + ")"))
    new_smry.append(str("=0.25*('Member Stats'!H" + str(i) + "+'Member Stats'!J" + str(i) + "+0.5*'Member Stats'!L" + str(i) + ")+MAX((13/40)*('Member Stats'!I" + str(i) + "+'Member Stats'!G" + str(i) + "),((13/40)*('Member Stats'!K" + str(i) + "*1.5)),((13/40)*('Member Stats'!M" + str(i) + "*1.5)))"))
    new_smry.append("='Member Stats'!J" + str(i))
    new_smry.append(str("=COUNTIF('Member Stats'!G" + str(i) + ":M" + str(i) + ",\">10\")"))
    new_smry.append(str("=IF(ISNUMBER('Member Stats'!C" + str(i) + "),IF(ISNUMBER('Member Stats'!D" + str(i) + "),\"UIM\",IF(ISNUMBER('Member Stats'!E" + str(i) + "),IF('Member Stats'!C" + str(i) + " > 'Member Stats'!E" + str(i) + ",\"Dead HCIM\",\"HCIM\"),\"IM\")),\"Normal\")"))
    new_smry.append(str("=IF(E" + str(i) + ">10,\"Clan Friend\",(IF(G" + str(i) + "=\"Normal\",(IF(F" + str(i) + "<1,(IF(C" + str(i) + ">=1500,\"Rune\",(IF(C" + str(i) + ">=1400,\"Adamant\",(IF(C" + str(i) + ">=1200,\"Mithril\",(IF(C" + str(i) + ">=900,\"Steel\",(IF(C" + str(i) + ">=600,\"Iron\",\"Bronze\")))))))))),(IF(F" + str(i) + "<3,(IF(C" + str(i) + ">=1666,\"Rune\",(IF(C" + str(i) + ">=1533,\"Adamant\",(IF(C" + str(i) + ">=1300,\"Mithril\",(IF(C" + str(i) + ">=966,\"Steel\",(IF(C" + str(i) + ">=633,\"Iron\",\"Bronze\")))))))))),(IF(F" + str(i) + "<5,(IF(C" + str(i) + ">=1833,\"Rune\",(IF(C" + str(i) + ">=1666,\"Adamant\",(IF(C" + str(i) + ">=1400,\"Mithril\",(IF(C" + str(i) + ">=1033,\"Steel\",(IF(C" + str(i) + ">=666,\"Iron\",\"Bronze\")))))))))),(IF(C" + str(i) + ">=2000,\"Rune\",(IF(C" + str(i) + ">=1800,\"Adamant\",(IF(C" + str(i) + ">=1500,\"Mithril\",(IF(C" + str(i) + ">=1100,\"Steel\",(IF(C" + str(i) + ">=700,\"Iron\",\"Bronze\")))))))))))))))),(IF(OR(G" + str(i) + "=\"IM\",G" + str(i) + "=\"Dead HCIM\",G" + str(i) + "=\"HCIM\"),(IF(F" + str(i) + "<1,(IF(C" + str(i) + ">=1500,\"Rune\",(IF(C" + str(i) + ">=1300,\"Adamant\",(IF(C" + str(i) + ">=1100,\"Mithril\",(IF(C" + str(i) + ">=800,\"Steel\",(IF(C" + str(i) + ">=500,\"Iron\",\"Bronze\")))))))))),(IF(F" + str(i) + "<3,(IF(C" + str(i) + ">=1666,\"Rune\",(IF(C" + str(i) + ">=1433,\"Adamant\",(IF(C" + str(i) + ">=1200,\"Mithril\",(IF(C" + str(i) + ">=866,\"Steel\",(IF(C" + str(i) + ">=533,\"Iron\",\"Bronze\")))))))))),(IF(F" + str(i) + "<5,(IF(C" + str(i) + ">=1833,\"Rune\",(IF(C" + str(i) + ">=1566,\"Adamant\",(IF(C" + str(i) + ">=1300,\"Mithril\",(IF(C" + str(i) + ">=933,\"Steel\",(IF(C" + str(i) + ">=566,\"Iron\",\"Bronze\")))))))))),(IF(C" + str(i) + ">=2000,\"Rune\",(IF(C" + str(i) + ">=1700,\"Adamant\",(IF(C" + str(i) + ">=1400,\"Mithril\",(IF(C" + str(i) + ">=1000,\"Steel\",(IF(C" + str(i) + ">=600,\"Iron\",\"Bronze\")))))))))))))))),(IF(G" + str(i) + "=\"UIM\",(IF(F" + str(i) + "<1,(IF(C" + str(i) + ">=1500,\"Rune\",(IF(C" + str(i) + ">=1200,\"Adamant\",(IF(C" + str(i) + ">=1000,\"Mithril\",(IF(C" + str(i) + ">=700,\"Steel\",(IF(C" + str(i) + ">=400,\"Iron\",\"Bronze\")))))))))),(IF(F" + str(i) + "<3,(IF(C" + str(i) + ">=1666,\"Rune\",(IF(C" + str(i) + ">=1333,\"Adamant\",(IF(C" + str(i) + ">=1100,\"Mithril\",(IF(C" + str(i) + ">=766,\"Steel\",(IF(C" + str(i) + ">=433,\"Iron\",\"Bronze\")))))))))),(IF(F" + str(i) + "<5,(IF(C" + str(i) + ">=1833,\"Rune\",(IF(C" + str(i) + ">=1466,\"Adamant\",(IF(C" + str(i) + ">=1200,\"Mithril\",(IF(C" + str(i) + ">=833,\"Steel\",(IF(C" + str(i) + ">=466,\"Iron\",\"Bronze\")))))))))),(IF(C" + str(i) + ">=2000,\"Rune\",(IF(C" + str(i) + ">=1600,\"Adamant\",(IF(C" + str(i) + ">=1300,\"Mithril\",(IF(C" + str(i) + ">=900,\"Steel\",(IF(C" + str(i) + ">=500,\"Iron\",\"Bronze\")))))))))))))))),\"ERROR\")))))))"))
    new_smry.append(str(""))
    new_smry.append(str(""))
    new_smry.append(str("=COUNTIF(Offences!A1:A,B" + str(i) + ")+COUNTIF(Offences!A1:A,A" + str(i) + ")"))
    new_smry.append(str(user.joined_at))
    new_smry.append(str(notes))

    sheet_stat.append_row(new_stats, "USER_ENTERED")
    sheet_smry.append_row(new_smry, "USER_ENTERED")

    await asyncio.sleep(1)
    recom_rank = sheet_smry.cell(i, 8).value

    await user.remove_roles(rune_role)
    await user.remove_roles(addy_role)
    await user.remove_roles(mith_role)
    await user.remove_roles(stel_role)
    await user.remove_roles(iron_role)
    await user.remove_roles(brnz_role)
    await user.remove_roles(frend_role)


    if str(recom_rank) == "Clan Friend":
        await ctx.send(rsn + " is no longer 10HP, giving Clan Friend rank to <@!" + str(user.id) + ">")
        await ctx.send("You can manually override this if desired to admit the member anyway")
        await user.add_roles(frend_role)
        sheet_smry.update_cell(i, 10, "Clan Friend")

    elif str(recom_rank) == "Bronze":
        await ctx.send(rsn + " is " + str(sheet_smry.cell(i, 3).value) + " total, giving Bronze rank to <@!" + str(user.id) + ">")
        await user.add_roles(brnz_role)
        sheet_smry.update_cell(i, 10, "Bronze")

    elif str(recom_rank) == "Iron":
        await ctx.send(rsn + " is " + str(sheet_smry.cell(i, 3).value)  + " total, giving Iron rank to <@!" + str(user.id) + ">")
        await user.add_roles(iron_role)
        sheet_smry.update_cell(i, 10, "Iron")

    elif str(recom_rank) == "Steel":
        await ctx.send(rsn + " is " + str(sheet_smry.cell(i, 3).value)  + " total, giving Steel rank to <@!" + str(user.id) + ">")
        await user.add_roles(stel_role)
        sheet_smry.update_cell(i, 10, "Steel")

    elif str(recom_rank) == "Mithril":
        await ctx.send(rsn + " is " + str(sheet_smry.cell(i, 3).value)  + " total, giving Mith rank to <@!" + str(user.id) + ">")
        await user.add_roles(mith_role)
        sheet_smry.update_cell(i, 10, "Mithril")

    elif str(recom_rank) == "Adamant":
        await ctx.send(rsn + " is " + str(sheet_smry.cell(i, 3).value)  + " total, giving Addy rank to <@!" + str(user.id) + ">")
        await user.add_roles(addy_role)
        sheet_smry.update_cell(i, 10, "Adamant")

    elif str(recom_rank) == "Rune":
        await ctx.send(rsn + " is " + str(sheet_smry.cell(i, 3).value)  + " total, giving Rune rank to <@!" + str(user.id) + ">")
        await user.add_roles(rune_role)
        sheet_smry.update_cell(i, 10, "Rune")

    await user.edit(nick=rsn)
    await ctx.send("You must also manually assign this rank ingame, <@!" + str(ctx.author.id) + ">")

    print(datetime.now())
    print(str(str(ctx.author) + " gave rank-up to " + str(user)))

@rankup.error
async def rankup_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Someone is requesting a rank-up. Please check if they have the appropriate levels. <@&" + str(os.getenv('leader')) + "> <@&" + str(os.getenv('council')) + ">")
        print(datetime.now())
        print(ctx.author, "attempted to use !rankup without permission")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide @DiscordUser")
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("Invalid Discord User")

@client.listen()
async def on_raw_reaction_add(payload):
    channel = client.get_channel(int(os.getenv('channel')))
    if payload.channel_id == int(os.getenv('reactchan')):
        if payload.message_id == int(os.getenv('reactmsg')):
            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = message.guild.get_member(payload.user_id)

            uimrole = discord.utils.get(message.guild.roles, name="UIM")
            hcimrole = discord.utils.get(message.guild.roles, name="HCIM")
            ironrole = discord.utils.get(message.guild.roles, name="IM")
            hp10role = discord.utils.get(message.guild.roles, name="10HP")
            skillrole = discord.utils.get(message.guild.roles, name="Skiller")
            f2prole = discord.utils.get(message.guild.roles, name="F2P")
            champrole = discord.utils.get(message.guild.roles, name="Champ Cape")

            if str(payload.emoji) == str(os.getenv('uim')):
                if uimrole not in user.roles:
                    print(user, "requested the role UIM")
                    await user.add_roles(uimrole)

            elif str(payload.emoji) == str(os.getenv('hcim')):
                if hcimrole not in user.roles:
                    print(user, "requested the role HCIM")
                    await user.add_roles(hcimrole)

            elif str(payload.emoji) == str(os.getenv('ironman')):
                if ironrole not in user.roles:
                    print(user, "requested the role IM")
                    await user.add_roles(ironrole)

            elif str(payload.emoji) == str(os.getenv('hp10')):
                if hp10role not in user.roles:
                    print(user, "requested the role 10HP")
                    await user.add_roles(hp10role)

            elif str(payload.emoji) == str(os.getenv('skiller')):
                if skillrole not in user.roles:
                    print(user, "requested the role Skiller")
                    await user.add_roles(skillrole)

            elif str(payload.emoji) == str(os.getenv('f2p')):
                if f2prole not in user.roles:
                    print(user, "requested the role F2P")
                    await user.add_roles(f2prole)

            elif str(payload.emoji) == str(os.getenv('champ')):
                if champrole not in user.roles:
                    print(user, "requested the role Champ Cape")
                    await user.add_roles(champrole)

            else:
                await message.remove_reaction(payload.emoji, payload.member)

@client.listen()
async def on_raw_reaction_remove(payload):
    channel = client.get_channel(int(os.getenv('channel')))
    if payload.channel_id == int(os.getenv('reactchan')):
        if payload.message_id == int(os.getenv('reactmsg')):
            channel = client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = message.guild.get_member(payload.user_id)

            uimrole = discord.utils.get(message.guild.roles, name="UIM")
            hcimrole = discord.utils.get(message.guild.roles, name="HCIM")
            ironrole = discord.utils.get(message.guild.roles, name="IM")
            hp10role = discord.utils.get(message.guild.roles, name="10HP")
            skillrole = discord.utils.get(message.guild.roles, name="Skiller")
            f2prole = discord.utils.get(message.guild.roles, name="F2P")
            champrole = discord.utils.get(message.guild.roles, name="Champ Cape")

            if str(payload.emoji) == str(os.getenv('uim')):
                if uimrole in user.roles:
                    print(user, "removed the role UIM")
                    await user.remove_roles(uimrole)

            elif str(payload.emoji) == str(os.getenv('hcim')):
                if hcimrole in user.roles:
                    print(user, "removed the role HCIM")
                    await user.remove_roles(hcimrole)

            elif str(payload.emoji) == str(os.getenv('ironman')):
                if ironrole in user.roles:
                    print(user, "removed the role IM")
                    await user.remove_roles(ironrole)

            elif str(payload.emoji) == str(os.getenv('hp10')):
                if hp10role in user.roles:
                    print(user, "removed the role 10HP")
                    await user.remove_roles(hp10role)

            elif str(payload.emoji) == str(os.getenv('skiller')):
                if skillrole in user.roles:
                    print(user, "removed the role Skiller")
                    await user.remove_roles(skillrole)

            elif str(payload.emoji) == str(os.getenv('f2p')):
                if f2prole in user.roles:
                    print(user, "removed the role F2P")
                    await user.remove_roles(f2prole)

            elif str(payload.emoji) == str(os.getenv('champ')):
                if champrole in user.roles:
                    print(user, "removed the role Champ Cape")
                    await user.remove_roles(champrole)

@client.command()
async def register(ctx, twitch_id: str):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    users_file = open("twitch_users.log", "r")
    users = users_file.readlines()
    users_file.close()
    users = [x.replace('\n', '') for x in users]

    i=0
    twitch_chans = []
    disc_ids = []
    for user in users:
        if i:
            i=0
            twitch_chans.append(user)
        else:
            i=1
            disc_ids.append(user)

    i=0
    for user in twitch_chans:
        if twitch_id.lower() == user.lower():
            await ctx.channel.send("The Twitch channel " + user + " is already registered to <@!" + disc_ids[i] + ">")
            return
        if int(disc_ids[i]) == ctx.author.id:
            await ctx.channel.send("You have already registered the Twitch channel " + user + ".\n Use !unregister to unregister this channel before registering a new one.")
            return
        i=i+1

    new_twitch = helix.user(twitch_id)
    if new_twitch:
        users_file = open("twitch_users.log", "a")
        users_file.write(str(str(ctx.author.id) + "\n"))
        users_file.write(str(twitch_id + "\n"))
        await ctx.channel.send("The Twitch channel " + twitch_id + " is now registered to <@!" + str(ctx.author.id) + ">")
        print(str(str(ctx.author) + " registered the Twitch cahnnel " + new_twitch.display_name))

    else:
        await ctx.channel.send("The Twitch channel " + twitch_id + " does not exist.")

@register.error
async def register_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide Twitch Channel to register")

@client.listen()
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!reminder":
        if message.author == client.user:
            if message.channel.id == int(os.getenv('botchan')):
                cc_chan = client.get_channel(int(os.getenv('channel')))
                await cc_chan.send('*Posture/Hydration Check! Sit Up Straight & Grab Yourself Some Water!')
        else:
            await message.channel.send('Posture/Hydration Check! Sit Up Straight & Grab Yourself Some Water!')
    else:
        return

@client.listen()
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!signup":
        if message.author == client.user:
            if message.channel.id == int(os.getenv('botchan')):
                cc_chan = client.get_channel(int(os.getenv('channel')))
                await cc_chan.send('*Use this in Discord to ping the mods/admins that you would like to join SOTW')
        else:
            if message.author.nick:
                name = message.author.nick
            else:
                name = message.author.name

            await message.channel.send(name + " would like to sign up for SOTW. Please check if they have passed introductory period and sign them up <@&" + str(os.getenv('leader')) + "> <@&" + str(os.getenv('council')) + ">")
    else:
        return

@client.listen()
async def on_message(message):
    if message.channel.id == int(os.getenv('channel')):
        return

    content = message.content
    if content.lower() == "!sotw":
        if message.author == client.user:
            if message.channel.id == int(os.getenv('botchan')):
                try:
                    sotw_file = open("sotw_cc.msg", "r")
                    sotw_msg = sotw_file.read()
                    sotw_file.close()
                except:
                    sotw_msg = "No sotw message is set"

                cc_chan = client.get_channel(int(os.getenv('channel')))
                await cc_chan.send(str('*' + sotw_msg))
        else:
            try:
                sotw_file = open("sotw_disc.msg", "r")
                sotw_msg = sotw_file.read()
                sotw_file.close()
            except:
                sotw_msg = "No sotw message is set"

            await message.channel.send(str(sotw_msg))
    else:
        return

@client.command()
@commands.has_permissions(manage_messages=True)
async def sotw_set(ctx, typ, sotw):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    if typ.lower() == "discord":
        sotw_file = open("sotw_disc.msg", "w")
        sotw_file.write(str(sotw))
        sotw_file.close()
        await ctx.send("SOTW Discord message set to:")
        sotw_file = open("sotw_disc.msg", "r")
        await ctx.send(str(sotw_file.read()))
        print(ctx.author, "set Discord sotw message to", sotw)
        sotw_file.close()

    elif typ.lower() == "cc":
        if len(sotw) > 79:
            await ctx.send("Message too long. Character limit is 79 for sotw cc message")
            await ctx.send(str("Your message is " + str(len(sotw)) + " characters"))
        else:
            sotw_file = open("sotw_cc.msg", "w")
            sotw_file.write(str(sotw))
            sotw_file.close()
            await ctx.send("SOTW CC message set to:")
            sotw_file = open("sotw_cc.msg", "r")
            await ctx.send(str(sotw_file.read()))
            print(ctx.author, "set CC sotw message to", sotw)
            sotw_file.close()

    else:
        await ctx.send("SotW type not valid. Specify either 'cc' or 'discord'")

@sotw_set.error
async def sotw_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide a message to set")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage messages to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !sotw_set without permission")

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
                    if hci_stats.skill('total', 'experience') == iron_stats.skill('total', 'experience'):
                        await ctx.send(rsn + " is a " + os.getenv('hcim'))
                    else:
                        await ctx.send(rsn + " is a " + os.getenv('ironman') + " (dead " + os.getenv('hcim') + ")")
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
        stats_edit.text((168,80), str(main_stats.skill('fishing', 'level')), (255, 255, 0), font=stats_font)

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

@client.command()
async def unregister(ctx, twitch_id: str):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    users_file = open("twitch_users.log", "r")
    users = users_file.readlines()
    users_file.close()
    users = [x.replace('\n', '') for x in users]

    i=0
    twitch_chans = []
    disc_ids = []
    for user in users:
        if i:
            i=0
            twitch_chans.append(user)
        else:
            i=1
            disc_ids.append(user)

    i=0
    for user in twitch_chans:
        if twitch_id.lower() == user.lower():
            if int(disc_ids[i]) == ctx.author.id:
                users_file = open("twitch_users.log", "r")
                users = users_file.readlines()
                users_file.close()
                users = [x.replace('\n', '') for x in users]

                users_file = open("twitch_users.log", "w")
                for twitch_user in users:
                    if user.lower() != twitch_user.lower():
                        if disc_ids[i] != twitch_user:
                            users_file.write(str(twitch_user + "\n"))
                users_file.close()

                await ctx.channel.send("The Twitch channel " + user + " has been unregistered from <@!" + disc_ids[i] + ">")
                return

            elif ctx.author.guild_permissions.manage_messages:
                users_file = open("twitch_users.log", "r")
                users = users_file.readlines()
                users_file.close()
                users = [x.replace('\n', '') for x in users]

                users_file = open("twitch_users.log", "w")
                for twitch_user in users:
                    if user.lower() != twitch_user.lower():
                        if disc_ids[i] != twitch_user:
                            users_file.write(str(twitch_user + "\n"))
                users_file.close()

                await ctx.channel.send("The Twitch channel " + user + " has been unregistered from <@!" + disc_ids[i] + ">")
                return

            else:
                await ctx.channel.send("The Twitch channel " + user + " is registered to <@!" + disc_ids[i] + ">\nYou cannot unregister someone elses channel")
                return

        i=i+1

    await ctx.channel.send("The twitch channel " + twitch_id + " is not registered.")

@unregister.error
async def unregister_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide Twitch Channel to unregister")

@client.listen()
async def on_member_join(member):
    welcome_chan = client.get_channel(int(os.getenv('welcome_channel')))
    #welcome_file = open("welcome.msg", "r")
    #await welcome_chan.send("Hey <@!" + str(member.id) + ">, welcome to **" + member.guild.name + "**!\n\n" + str(welcome_file.read()))
    #print(member.name, "joined the server")
    #welcome_file.close()

    unverified = discord.utils.get(member.guild.roles, name="unverified")
    await member.add_roles(unverified)
    await welcome_chan.send("Hey <@!" + str(member.id) + ">, welcome to **" + member.guild.name + "**!\n" + "To gain full discord access open an application in <#874291551688335430>")

@client.command()
@commands.has_permissions(manage_messages=True)
async def welcome_set(ctx, welcome):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    welcome_file = open("welcome.msg", "w")
    welcome_file.write(str(welcome))
    welcome_file.close()
    await ctx.send("Discord Welcome message set to:")
    welcome_file = open("welcome.msg", "r")
    welcome_msg = str("Hey <@!" + str(ctx.message.author.id) + ">, welcome to **" + ctx.guild.name + "**!" + "\n\n" + str(welcome_file.read()))
    welcome_file.close()

    if len(welcome) > 1925:
        await ctx.send("Message too long. Max length is 1925 characters, must allow room to @user at start")
        await ctx.send("Your message is " + str(len(welcome)) + " characters")
    else:
        await ctx.send(welcome_msg)
        print(ctx.author, "set Discord welcome message to", welcome)

@welcome_set.error
async def welcome_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide a message to set")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage messages to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !welcome_set without permission")

@client.command()
@commands.has_permissions(manage_messages=True)
async def move(ctx, channel: discord.TextChannel, *message_ids: int):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    for message_id in message_ids:
        message = await ctx.channel.fetch_message(message_id)

        if not message:
            ctx.send("That message id does not exist")
        else:
            if message.attachments:
                attach = await message.attachments[0].to_file()
                await channel.send("**Moved from <#" + str(message.channel.id) + "> -** <@" + str(message.author.id) + ">: " + message.content, file=attach)
            else:
                await channel.send("**Moved from <#" + str(message.channel.id) + "> -** <@" + str(message.author.id) + ">: " + message.content)

            print(datetime.now())
            print(ctx.author, "moved a message from", message.channel.name, "to", channel.name)
            print(message.author.name, "-", message.content)
            await message.delete()
            await ctx.message.delete()

@move.error
async def move_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide #Channel and message ids")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage messages to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !move without permission")

client.run(os.getenv('TOKEN'))
