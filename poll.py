#!/bin/python3 -u
import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
import asyncio
import matplotlib.pyplot as plt
import numpy as np

load_dotenv()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('!poll started on bot {0.user}'.format(client))


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

client.run(os.getenv('TOKEN'))
