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
    print('!rankup started on bot {0.user}'.format(client))


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

    brnze_role = discord.utils.get(ctx.guild.roles, name="Bronze")
    nana3_role = discord.utils.get(ctx.guild.roles, name="🍌🍌🍌")
    nana2_role = discord.utils.get(ctx.guild.roles, name="🍌🍌")
    nana1_role = discord.utils.get(ctx.guild.roles, name="🍌")
    aplct_role = discord.utils.get(ctx.guild.roles, name="Applicant")
    frend_role = discord.utils.get(ctx.guild.roles, name="Clan Friend")
    leadr_role = discord.utils.get(ctx.guild.roles, name="Leader")
    concl_role = discord.utils.get(ctx.guild.roles, name="Council")

    if brnze_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is already Bronze, can't rank-up any further.")
        return
    
    elif nana3_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is already 3 Banana. Bronze rank-ups must be done manually.")
        return

    elif nana2_role in user.roles:
        ready=1
    
    elif nana1_role in user.roles:
        ready=1

    elif aplct_role in user.roles:
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
        await ctx.send("<@!" + str(user.id) + "> has no rank. Use !giverank to add new members")
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
    new_smry.append(str("=COUNTIF('Member Stats'!G" + str(i) + ":AC" + str(i) + ",99)"))
    new_smry.append(str("=IF(ISNUMBER('Member Stats'!C" + str(i) + "),IF(ISNUMBER('Member Stats'!D" + str(i) + "),\"UIM\",IF(ISNUMBER('Member Stats'!E" + str(i) + "),IF('Member Stats'!C" + str(i) + " > 'Member Stats'!E" + str(i) + ",\"Dead HCIM\",\"HCIM\"),\"Iron\")),\"Normal\")"))
    new_smry.append(str("=IF(E" + str(i) + ">10,\"Clan Friend\",IF(AND(C" + str(i) + "<900,G" + str(i) + "=\"Normal\"),\"Applicant\",IF(AND(C" + str(i) + "<1250,G" + str(i) + "=\"Normal\"),\"1 Banana\",IF(AND(C" + str(i) + "<1400,G" + str(i) + "=\"Normal\"),\"2 Banana\",IF(AND(C" + str(i) + "<2277,G" + str(i) + "=\"Normal\"),\"3 Banana\",IF(AND(C" + str(i) + "<750,G" + str(i) + "=\"Normal\",D" + str(i) + "<4),\"Applicant\",IF(AND(C" + str(i) + "<1100,G" + str(i) + "=\"Normal\",D" + str(i) + "<4),\"1 Banana\",IF(AND(C" + str(i) + "<1250,G" + str(i) + "=\"Normal\",D" + str(i) + "<4),\"2 Banana\",IF(AND(C" + str(i) + "<2277,G" + str(i) + "=\"Normal\",D" + str(i) + "<4),\"3 Banana\",IF(AND(C" + str(i) + "<750,OR(G" + str(i) + "=\"Iron\",G" + str(i) + "=\"HCIM\",G" + str(i) + "=\"Dead HCIM\")),\"Applicant\",IF(AND(C" + str(i) + "<1000,OR(G" + str(i) + "=\"Iron\",G" + str(i) + "=\"HCIM\",G" + str(i) + "=\"Dead HCIM\")),\"1 Banana\",IF(AND(C" + str(i) + "<1150,OR(G" + str(i) + "=\"Iron\",G" + str(i) + "=\"HCIM\",G" + str(i) + "=\"Dead HCIM\")),\"2 Banana\",IF(AND(C" + str(i) + "<2277,OR(G" + str(i) + "=\"Iron\",G" + str(i) + "=\"HCIM\",G" + str(i) + "=\"Dead HCIM\")),\"3 Banana\",IF(AND(C" + str(i) + "<650,G" + str(i) + "=\"UIM\"),\"Applicant\",IF(AND(C" + str(i) + "<900,G" + str(i) + "=\"UIM\"),\"1 Banana\",IF(AND(C" + str(i) + "<1050,G" + str(i) + "=\"UIM\"),\"2 Banana\",IF(AND(C" + str(i) + "<2277,G" + str(i) + "=\"UIM\"),\"3 Banana\",\"ERROR\")))))))))))))))))"))
    new_smry.append(str(""))
    new_smry.append(str(""))
    new_smry.append(str("=COUNTIF(Offences!A1:A,B" + str(i) + ")+COUNTIF(Offences!A1:A,A" + str(i) + ")"))
    new_smry.append(str(user.joined_at))
    new_smry.append(str(notes))

    sheet_stat.append_row(new_stats, "USER_ENTERED")
    sheet_smry.append_row(new_smry, "USER_ENTERED")

    await asyncio.sleep(1)
    recom_rank = sheet_smry.cell(i, 8).value

    if str(recom_rank) == "Clan Friend":
        await ctx.send(rsn + " is not 10HP, giving Clan Friend rank to <@!" + str(user.id) + ">")
        await ctx.send("You can manually override this if desired to admit the member anyway")
        await user.add_roles(frend_role)
        await user.remove_roles(aplct_role)
        await user.remove_roles(nana1_role)
        await user.remove_roles(nana2_role)
        await user.remove_roles(nana3_role)
        sheet_smry.update_cell(i, 10, "Clan Friend")

    elif str(recom_rank) == "Applicant":
        await ctx.send(rsn + " is " + str(sheet_smry.cell(i, 3).value) + " total, giving Applicant rank to <@!" + str(user.id) + ">")
        await user.add_roles(aplct_role)
        await user.remove_roles(nana1_role)
        await user.remove_roles(nana2_role)
        await user.remove_roles(nana3_role)
        await user.remove_roles(frend_role)
        sheet_smry.update_cell(i, 10, "Applicant")

    elif str(recom_rank) == "1 Banana":
        await ctx.send(rsn + " is " + str(sheet_smry.cell(i, 3).value)  + " total, giving 1 Banana rank to <@!" + str(user.id) + ">")
        await user.add_roles(nana1_role)
        await user.remove_roles(aplct_role)
        await user.remove_roles(nana2_role)
        await user.remove_roles(nana3_role)
        await user.remove_roles(frend_role)
        sheet_smry.update_cell(i, 10, "1 Banana")

    elif str(recom_rank) == "2 Banana":
        await ctx.send(rsn + " is " + str(sheet_smry.cell(i, 3).value)  + " total, giving 2 Banana rank to <@!" + str(user.id) + ">")
        await user.add_roles(nana2_role)
        await user.remove_roles(aplct_role)
        await user.remove_roles(nana1_role)
        await user.remove_roles(nana3_role)
        await user.remove_roles(frend_role)
        sheet_smry.update_cell(i, 10, "2 Banana")

    elif str(recom_rank) == "3 Banana":
        await ctx.send(rsn + " is " + str(sheet_smry.cell(i, 3).value)  + " total, giving 3 Banana rank to <@!" + str(user.id) + ">")
        await user.add_roles(nana3_role)
        await user.remove_roles(aplct_role)
        await user.remove_roles(nana1_role)
        await user.remove_roles(nana2_role)
        await user.remove_roles(frend_role)
        sheet_smry.update_cell(i, 10, "3 Banana")

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

client.run(os.getenv('TOKEN'))
