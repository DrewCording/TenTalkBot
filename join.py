#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import asyncio
from datetime import datetime
from datetime import date

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!join started on bot {0.user}'.format(client))


@client.command()
@commands.has_permissions(manage_roles=True)
async def join(ctx, user: discord.Member, name: str, role: str):
    if ctx.channel.id == int(os.getenv('channel')):
        return

    stdnt_role = discord.utils.get(ctx.guild.roles, name="Student")
    teach_role = discord.utils.get(ctx.guild.roles, name="Teaching Assistant")
    alumn_role = discord.utils.get(ctx.guild.roles, name="Alumni")
    fclty_role = discord.utils.get(ctx.guild.roles, name="Faculty")
    frend_role = discord.utils.get(ctx.guild.roles, name="Friend")
    modrt_role = discord.utils.get(ctx.guild.roles, name="Mod")
    admin_role = discord.utils.get(ctx.guild.roles, name="Admin")

    if stdnt_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is already a member of this server.")
        return
    
    elif teach_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is already a member of this server.")
        return

    elif alumn_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is already a member of this server.")
        return
    
    elif fclty_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is already a member of this server.")
        return

    elif modrt_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is already a member of this server.")
        return

    elif admin_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is already a member of this server.")
        return

    elif frend_role in user.roles:
        await ctx.send("<@!" + str(user.id) + "> is already a member of this server.")
        return

    await user.edit(nick=name)
    
    if str(role.lower()) == "student":
        await ctx.send("Welcome <@!" + str(user.id) + "> to the server. You have been given the role Student.")
        await user.add_roles(stdnt_role)

    elif str(role.lower()) == "ta":
        await ctx.send("Welcome <@!" + str(user.id) + "> to the server. You have been given the role Teaching Assistant.")
        await user.add_roles(teach_role)

    elif str(role.lower()) == "alumni":
        await ctx.send("Welcome <@!" + str(user.id) + "> to the server. You have been given the role Alumni.")
        await user.add_roles(alumn_role)

    elif str(role.lower()) == "faculty":
        await ctx.send("Welcome <@!" + str(user.id) + "> to the server. You have been given the role Faculty.")
        await user.add_roles(fclty_role)

    elif str(role.lower()) == "friend":
        await ctx.send("Welcome <@!" + str(user.id) + "> to the server. You have been given the role Friend.")
        await user.add_roles(frend_role)

    else: 
        await ctx.send("That is not a valid role <@!" + str(ctx.author.id) + ">. Role must be one of: Friend, Student, TA, Alumni, Faculty.")
        return

    await user.edit(nick=name)
    print(datetime.now())
    print(str(str(ctx.author) + " gave membership to " + str(user) + " with name " + name))

@join.error
async def join_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage roles to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !join without permission")
    elif isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide @DiscordUser, name, and role")
    elif isinstance(error, discord.ext.commands.errors.MemberNotFound):
        await ctx.send("Invalid Discord User")

client.run(os.getenv('TOKEN'))
