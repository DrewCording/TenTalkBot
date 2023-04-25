#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
import asyncio

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!verify started on bot {0.user}'.format(client))


@client.command()
#@commands.has_permissions(manage_roles=True)
async def verify(ctx, user: discord.Member):
    if ctx.channel.category_id == int(os.getenv('app_cat')):
        verified = discord.utils.get(ctx.guild.roles, name="verified")
        unverified = discord.utils.get(ctx.guild.roles, name="unverified")

        if verified not in user.roles:
            if unverified in user.roles:
                await user.remove_roles(unverified)
                await user.add_roles(verified)
                await ctx.send("<@!" + str(user.id) + "> is now verified. \nThis channel will self-destruct in 2 minutes")

                apps_file = open("open_apps.log", "r")
                apps_list = apps_file.readlines()
                apps_file.close()

                apps_list = list(map(str.strip,apps_list))
                
                if str(ctx.channel.id) in apps_list:
                    apps_list.remove(str(ctx.channel.id))
                    apps_file = open("open_apps.log", "w")
                    for items in apps_list:
                        apps_file.write(str(items + "\n"))
                    apps_file.close()

                await asyncio.sleep(120)
                await ctx.channel.delete()

        else: 
            await ctx.send("<@!" + str(user.id) + "> is already verified")
    else: 
        await ctx.send("You can only use this in an application thread")


@verify.error
async def verify_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        await ctx.send("Must provide @user to verify")
    if isinstance(error, discord.ext.commands.errors.MissingPermissions):
        await ctx.send("Must be able to manage roles to run this command. This has been reported")
        print(datetime.now())
        print(ctx.author, "attempted to use !verify without permission")

client.run(os.getenv('TOKEN'))
