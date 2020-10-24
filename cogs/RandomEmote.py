import asyncio
import datetime
import discord
from discord.ext import commands
import json
import random
import threading
import sys
sys.path.append(".")

class RandomEmote(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #import json file
    DATA = json.load(open("data/emoji.json", "r"))
    #Random emote
    FUNNY_EMOTE = str(random.choice(list(DATA.values()))['code_points']['base']).split("-")

    async def generate_emote(self):
        emote = random.choice(list(self.DATA.values()))
        #make it not racist
        if not "tone" in emote['shortname']:
            return emote['shortname']
        else:
            split_emote = emote['shortname'].split("_")
            new_emote = ""
            for word in split_emote:
                if "tone" in word:
                    new_emote += ":"
                else:
                    new_emote+= word + "_"
            return new_emote[:len(new_emote)-2] + ":"

    #This command picks a random emote and prints it to the channel
    @commands.command(pass_context=True)
    async def emoteroll(self, ctx):
        funny_emote = await self.generate_emote()
        await ctx.send("`Funny emote:` ")
        await ctx.send(funny_emote)

    async def daily_emote(self):
        print("function test")
        await channel.send("`Funny emote:`")
        await channel.send(await self.generate_emote())

    #The loop that sets a new funny emote to the status
    async def timeoutLoop(self):
        while True:
            time_now = datetime.datetime.now()
            #If it is midnight, reset funny_emote
            if time_now.hour == 0:
                print("Doing the thing!")
                self.FUNNY_EMOTE = str(random.choice(list(self.DATA.values()))['code_points']['base']).split("-")
                await self.bot.change_presence(activity=(discord.Game(name = "g<" + " " + chr(int(self.FUNNY_EMOTE[0], 16)))))
                channel = self.bot.get_channel(738728637376757780)
                await channel.send("`Funny Emote:`")
                await channel.send(chr(int(self.FUNNY_EMOTE[0], 16)))
                await asyncio.sleep(600)
            else:
                await asyncio.sleep(600)

    #starts the timeoutLoop function on a thread loop
    async def multiThreadDrifting(self):
        loop = asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(await self.timeoutLoop())

def setup(bot):
    bot.add_cog(RandomEmote(bot))
