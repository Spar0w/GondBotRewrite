from __future__ import unicode_literals
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import datetime
import sys
sys.path.append("./cogs")
from RandomEmote import RandomEmote

#Setup

PREFIX = 'g<'
bot = commands.Bot(command_prefix = PREFIX)

#Get's the time right now
startTime = datetime.datetime.now()

#Token
TOKEN = 'token lol'
emoji=chr(int(RandomEmote.FUNNY_EMOTE[0], 16))

#list of cogs
cogs = ['cogs.Generic', 'cogs.Translate', 'cogs.Images', 'cogs.RandomEmote', 'cogs.Chad', 'cogs.Supervisor']

#The setup event. Loads the cogs, sends the start message, and adds the presence
@bot.event
async def on_ready():
    ranE = RandomEmote(bot)
    asyncio.ensure_future(ranE.multiThreadDrifting())
    #Load the cogs
    for cog in cogs:
        bot.load_extension(cog)
    #Start message
    print('Im ' + bot.user.name + ', and I am cooler than you at ' + str(startTime))
    print(discord.__version__)

#Reload command. Reloads a specified cog, only I call the command
@bot.command(name='reload', hidden=True)
async def reload(ctx, cog: str):
    if ctx.author.id == 180340046287601665: #My unique ID
        try:
            #Reload the extension
            bot.reload_extension(f"cogs.{cog}")
            #Let the user know that the cog has been reloaded
            print(cog + " has been reloaded")
            await ctx.send(f"`{cog} has been reloaded`")
        except SyntaxError as se:
            await ctx.send(e)
        except Exception as e:
            print(e)
    else:
        #Log if someone who is not me trys to reload a cog
        print(ctx.author + "is naughty")

bot.run(TOKEN, bot=True, reconnect=True)

