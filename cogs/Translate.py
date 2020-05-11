import discord
from discord.ext import commands
import googletrans
from googletrans import Translator
import re

class Translate(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Use google translate to select a language and translate it

    @commands.command(pass_context=True)
    async def translate(self, ctx, startLang, endLang, *words):
            translator = Translator() #New translator object
            begin = ' '.join(words) #Joins the input into one string
            try:
                await ctx.send("`Translating ...`") 
                await ctx.trigger_typing() #Show typing in discord
                translated = translator.translate(begin, src=startLang, dest=endLang) #Translate the message
                result = str(translated) # convert to a string
                end = re.match(r".*?text=(.*)\, p.*", result) #extract the result
                await ctx.send(end.group(1)) #Send the translated message
            except ValueError as valerr:
                if(str(valerr) == "Expecting value: line 1 column 1 (char 0)"):
                    await ctx.send("Your input is fucked")
                elif(str(valerr) == "invalid destination language"):
                    await ctx.send("I don't recognize those language codes!")

    @translate.error
    async def translateErrors(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            await ctx.send("Please enter that languages you want to have translated! Format: Lang Code, Lang Code, Message")

    #Translate back and forth between Chinese and Russian for a while and then back into English.
    @commands.command(pass_context=True)
    async def obfuscate(self, ctx, *words):
        powerLevel = 2
        translator = Translator()
        begin = str(' '.join(words))
        langs = ["en", "zh-CN", "ru", "ja", "am", "fi", "es", "en"] #List of langs to cycle through. Start and end needs to be the same
        try:
            await ctx.send("`Obfuscating ...`") 
            await ctx.trigger_typing() #Show typing on discord
            y=0
            while y < int(powerLevel):
                x=0
                while x <= len(langs)-2:
                    translate = translator.translate(begin, src=langs[x], dest=langs[x+1]) #translate 
                    translate = re.match(r".*?text=(.*)\, p.*", str(translate)) #get the result
                    begin = str(translate.group(1)) #change begin to the newly translated message
                    x+=1
                y+=1

            await ctx.send(begin) #Sends the obfuscated message
        
        except ValueError as valerr:
            if(str(valerr) == "Expecting value: line 1 column 1 (char 0)"):
                await ctx.send("Your input is fucked")
            else:
                await ctx.send("Please enter text to be translated and your power level. Format: Power Level < 3, Message")

def setup(bot):
    bot.add_cog(Translate(bot))
