#!/bin/python3 -u
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
async def rankup(ctx, user: discord.Member):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    flag = 0
    testrole = discord.utils.find(lambda r: r.name == "Applicant", ctx.guild.roles)
    if testrole in user.roles:
        newrank = discord.utils.get(ctx.guild.roles, name="🍌")
        oldrank = discord.utils.get(ctx.guild.roles, name="Applicant")
        await user.add_roles(newrank)
        await user.remove_roles(oldrank)
        await ctx.send(str(format(user.name) + " ranked up from Applicant to 🍌"))
        flag = 1

    testrole = discord.utils.find(lambda r: r.name == "🍌", ctx.guild.roles)
    if testrole in user.roles:
        newrank = discord.utils.get(ctx.guild.roles, name="🍌🍌")
        oldrank = discord.utils.get(ctx.guild.roles, name="🍌")
        await user.add_roles(newrank)
        await user.remove_roles(oldrank)
        await ctx.send(str(format(user.name) + " ranked up from 🍌 to 🍌🍌"))
        flag = 1

    testrole = discord.utils.find(lambda r: r.name == "🍌🍌", ctx.guild.roles)
    if testrole in user.roles:
        newrank = discord.utils.get(ctx.guild.roles, name="🍌🍌🍌")
        oldrank = discord.utils.get(ctx.guild.roles, name="🍌🍌")
        await user.add_roles(newrank)
        await user.remove_roles(oldrank)
        await ctx.send(str(format(user.name) + " ranked up from 🍌🍌 to 🍌🍌🍌"))
        flag = 1

    testrole = discord.utils.find(lambda r: r.name == "🍌🍌🍌", ctx.guild.roles)
    if testrole in user.roles:
        newrank = discord.utils.get(ctx.guild.roles, name="Bronze")
        oldrank = discord.utils.get(ctx.guild.roles, name="🍌🍌🍌")
        await user.add_roles(newrank)
        await user.remove_roles(oldrank)
        await ctx.send(str(format(user.name) + " ranked up from 🍌🍌🍌 to Bronze"))
        flag = 1

    testrole = discord.utils.find(lambda r: r.name == "Bronze", ctx.guild.roles)
    if testrole in user.roles:
        await ctx.send(str(format(user.name) + " is already Bronze!"))
        flag = 1

    if flag == 0:
        await ctx.send("Rankup failed. User must already have a rank to rankup")

@rankup.error
async def rankup_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("User does not exist")
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide @User")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage roles to run this command")

client.run(os.getenv('TOKEN'))
