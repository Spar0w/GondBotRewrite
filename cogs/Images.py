import discord
from discord.ext import commands
import aiohttp
from google_images_download import google_images_download
import json
import random

class Images(commands.Cog):

    response = google_images_download.googleimagesdownload()

    def __init__(self, bot):
        self.bot = bot

    def query_monkey(self):
        monkey_kinds = ["monkeys", "cool monkeys", "monkey", "awesome monkey", "monkey in tree", "funny monkey"]
        return random.choice(monkey_kinds)

    #Pull a list of URLs from google images
    async def find_monkey(self):
        arguments = {"keywords":self.query_monkey(),"limit":100,"no_download":True}
        try:
            monkeys = self.response.download(arguments)
        except:
            print("lol")
        #Convert the outputed tuple into a string
        monkeys = str(monkeys)
        try:
            #Convert the string output to an array
            monkey_list = monkeys[21:-5]
            monkey_list = monkey_list.strip('][').split(', ')
            return monkey_list
        except IndexError:
            await ctx.send("`Something went wrong lol`")

    #Loads from my personal gondola collection
    @commands.command(pass_context=True)
    async def gondola(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://spar0w.xyz/rangond.php') as img:
                if img.status == 200:
                    await ctx.send(await img.text())
                else:
                    await ctx.send("bot broke lmao")

    #Pull a URL from google images of a monkey and post that url
    @commands.command(pass_context=True)
    async def monkey(self, ctx):
        try:
            monkey_list = await self.find_monkey()
            #Get a random monkey image from the result
            ran_num = random.randint(0, len(monkey_list))
            monkey_pic = monkey_list[ran_num]
            #Send the image
            await ctx.send(monkey_pic[1:-1])
        except IndexError:
            await ctx.send("`Something went wrong lol`")



def setup(bot):
    bot.add_cog(Images(bot))
