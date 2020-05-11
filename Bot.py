from __future__ import unicode_literals 
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import datetime 
from datetime import time

#Setup

PREFIX = 'g<'
bot = commands.Bot(command_prefix = PREFIX)
#WORDS = json.loads(open('/home/Bot/dictionary-master/dictionary.json', encoding='utf-8').read())#May switch to another json file. Shouldn't effect the function tho.

#Get's the time right now
startTime = datetime.datetime.now()

#Token
TOKEN = 'token lmao'

#list of cogs
cogs = ['cogs.Generic', 'cogs.Audio', 'cogs.Translate', 'cogs.Images']

#The setup event. Loads the cogs, sends the start message, and adds the presence
@bot.event
async def on_ready():
    #Load the cogs
    for cog in cogs:
        bot.load_extension(cog)
    #Start message
    print('Im ' + bot.user.name + ', and I am cooler than you at ' + str(startTime))
    print(discord.__version__)
    #Change the bot's presence
    await bot.change_presence(activity=discord.Game(name=PREFIX))
    return

#Reload command. Reloads a specified cog, only I call the command
@bot.command()
async def reload(ctx, cog: str):
    if ctx.author.id == 180340046287601665: #My unique ID
        try:
            #Reload the extension
            bot.reload_extension(f"cogs.{cog}")
            #Let the user know that the cog has been reloaded
            print(cog + " has been reloaded")
            await ctx.send(f"`{cog} has been reloaded`")
        except Exception as e:
            print(e)
    else:
        #Log if someone who is not me trys to reload a cog
        print(ctx.author + "is naughty")

bot.run(TOKEN)

