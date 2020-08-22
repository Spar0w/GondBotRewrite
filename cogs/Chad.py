import discord
from discord.ext import commands
import os
from wand.image import Image
from wand.font import Font

#This is the general Image manipulation class. More commands could be added in the future,
#but for now, it just contains commands to run the chad command
class Chad(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Function to pull the last message that was sent in the channel
    async def pull_messages(self, ctx, response='default'):
        if response == 'default' or response.lower() == 'yes' or response.lower() == 'no':
            messages = await ctx.channel.history(limit=5).flatten() #Pull the last 5 messages from the channel history
            captions = [str(messages[2].content), str(messages[1].content)] #The last two messages before the command was run
        else:
            messages = await ctx.channel.history(limit=3).flatten()
            captions = [str(messages[1].content), str(response)] #if there is user input, load the last message and the input into captions
        return(captions) #Return the conent of the messages before the command was run

    #Function to add text to the image template
    async def chad_magic(self, ctx, response):
        #Initialize Variables
        text = await self.pull_messages(ctx, response)
        x = 200 #The x coord of the caption
        y = 150 #The y coord of the caption
        width = 500 #the width of the caption
        height = 225 #the height of the caption
        font = Font('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf') #Random font that ill use just for now

        #Determine the response from the command
        if response.lower() == 'yes': #Load the Yes template if yes is a parameter
            template = 'data/chadtemplateyes.png'
        elif response.lower() == 'no': #Load the No template if no is a parameter
            template = 'data/chadtemplateno.png'
        else: #If not load the normal template
            template = 'data/chadtemplate.png'

        #Create the image
        with Image(filename=template) as img: #Load the original image
            with img.clone() as clonedimage: #Clone the image for manipulation
                if template == 'data/chadtemplate.png': #If the default option gets loaded up
                    clonedimage.caption(text[0], x, y, width, height, font) #Add the caption to the image
                    clonedimage.caption(text[1], x+1085, y+700, width, height, font) #Add the caption response to the image
                else: #If the default option is not loaded
                    clonedimage.caption(text[1], x, y, width, height, font) #Add the caption to the image
                clonedimage.save(filename='data/response.png') #Save the file.

    #The command that will run the pull_message() function and the the image manipulation function
    @commands.command()
    async def chad(self, ctx, *response):
        try:
            if type(response) == tuple: #If the input is a few words
                response = (' '.join(response)) #Join them in one string
                if not response: #If there is no input
                    response = 'default' #make it default
        await self.chad_magic(ctx, response) #Creates the image
        with open('data/response.png', 'rb') as response:
            await ctx.send(file=discord.File(response, 'post.png')) #This sends send the modified image into the channel

def setup(bot):
    bot.add_cog(Chad(bot))

