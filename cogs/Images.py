import discord
from discord.ext import commands
import aiohttp

class Images(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Loads from my personal gondola collection
    @commands.command(pass_context=True)
    async def gondola(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://spar0w.xyz/rangond.php') as img:
                if img.status == 200:
                    await ctx.send(await img.text())
                else:
                    await ctx.send("bot broke lmao")

def setup(bot):
    bot.add_cog(Images(bot))
