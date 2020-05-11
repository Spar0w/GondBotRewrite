import datetime
from datetime import datetime
from discord.ext import commands
import random

class Generic(commands.Cog):
    #Conventional Shit

    def __init__(self, bot):
        self.bot = bot

    #basic ping command that tests to see if the bot is working 
    @commands.command()
    async def ping(self, ctx):
        start = datetime.timestamp(datetime.now()) #Starts the ping
        await ctx.send('Ping :ping_pong: Pong  `{0}ms`'.format( #Ends the ping and formats it
                                                            round((datetime.timestamp(datetime.now()) - start) * 1000000))) 
        print(ctx.message.author.name + ' has pinged.') #Logs who pinged
        return

    #Chooses from a list of options that would come up in an eight ball and outputs it
    @commands.command(name="8ball")
    async def eightball(self, ctx):
        #Define list of responces 
        possible_responses = [ 
            'Absolutely No',
            'Not likely',
            "I'm not quite sure",
            'Definetly yes',
            'Maybe',
            'Probably',
            'Probably Not'
        ]
        await ctx.send(random.choice(possible_responses) + ", " + ctx.message.author.mention) #Displays the randomized message
        return

    #Chooses one of three messages (one is a xD funny refrence) and outputs it as a side of a coin
    #No coin emote so I spelt it out
    @commands.command()
    async def cointoss(ctx):
        random.seed(10)
        coin = ["The coin landed in between two tiles", "Heads", "Tails"] #The choices for the coin
        await ctx.send("" + random.SystemRandom().choice(coin)) #Displays the random coin
        return

    #Comes up with a random number from 1 to 6 and outputs it with a dice emote
    @commands.command()
    async def diceroll(self, ctx):
        random.seed(10) 
        await ctx.send(":game_die:" + str(random.SystemRandom().randrange(1,6)))

    #The poll function. For basic polling on a message.
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('g<poll'):
            reactions = ["\U0001F44D", "\U0001F914", "\U0001F44E"] #unicode for up, thinking, down
            for react in reactions:
                await message.add_reaction(react)
        
def setup(bot):
    bot.add_cog(Generic(bot))
