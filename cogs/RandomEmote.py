import discord
from discord.ext import commands
import json
import random
import sys
sys.path.append(".")

class RandomEmote(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #import json file
    DATA = json.load(open("data/eac.json", "r"))
    #Random emote
    FUNNY_EMOTE = random.choice(list(DATA.values()))

    def generate_emote(self):
        emote=random.choice(list(self.DATA.values()))
        return emote['alpha_code']

    #This command picks a random emote and prints it to the channel
    @commands.command(pass_context=True)
    async def emoteroll(self, ctx):
        funny_emote = self.generate_emote()
        await ctx.send("`Funny emote:` ")
        await ctx.send(funny_emote)

    async def daily_emote(self):
        print("function test")
        channel = self.bot.get_channel(738728637376757780)
        await channel.send("`Funny emote:`")
        await channel.send(self.generate_emote())

def setup(bot):
    bot.add_cog(RandomEmote(bot))
