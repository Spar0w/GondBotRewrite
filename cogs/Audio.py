import discord
from discord.ext import commands
import asyncio
import datetime
from datetime import time
import youtube_dl
import opuslib
import re
import requests
import threading
from threading import Timer

class Audio(commands.Cog):

    PLAYERS={}

    def __init__(self, bot):
        self.bot = bot

    #The loop that determines if the bot should leave the voice channel or not based on inactivity
    async def timeoutLoop(self, ctx, vc):
        startTime = datetime.datetime.now() #reset startTime
        while True:
            endTime = datetime.datetime.now() #This will be set every loop to determine inactivity. 
            if((endTime.minute - startTime.minute) >= 5): #if the time is above 5 minutes
                if vc.is_playing(): 
                    startTime = datetime.datetime.now() #if the bot is playing something, reset the timer
                    await asyncio.sleep(60)
                else:
                    await self.PLAYERS['0'].disconnect() #if it is not playing, disconnect and break the loop
                    break
            elif vc.is_playing():
                startTime = datetime.datetime.now()
                await asyncio.sleep(60)
            elif not self.PLAYERS['0'].is_connected(): #breaks the loop if the bot is not connected to a voice channel
                break
            else:
                await asyncio.sleep(60) #loop every 60 seconds

    #starts the timeoutLoop function on a thread loop
    def multiThreadDrifting(self, ctx, vc, loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.timeoutLoop(ctx, vc))

    #starts the thread
    async def startThread(self, ctx, vc):
        loop = asyncio.get_event_loop()
        t = threading.Thread(target = self.multiThreadDrifting, args=(ctx, vc, loop))
        t.start()

    #join the voice channel
    async def joinVoice(self, ctx):
        startTime = datetime.datetime.now() #Save when the bot joined the voice channel
        author = ctx.author 
        channel = author.voice.channel
        vc = await channel.connect()
        try:
            self.PLAYERS['0'] = vc
        except:
            await ctx.send("fuck")
        await self.startThread(ctx, vc) #start the thread that will run the timeoutLoop

    #This command calls the joinVoice method.
    @commands.command()
    async def join(self, ctx):
        await self.joinVoice(ctx)

    #Youtube link -> Audio stream
    #takes a link to a youtube-dl compatable link and streams it to the user's voice channel
    @commands.command()
    async def play(self, ctx, *url):
        if self.voiceChecker(ctx) == True:
            startTime = datetime.datetime.now() #reset startTime
            search = (' '.join(url))
            try:
                await self.joinVoice(ctx) #join the voice chanel
            except:
                #prevents the bot from moving channels
                print("already connected to voice server") 
            #Prevents playlists from being downloaded. instead extracts the url for the real video
            if "&list=" in search:
                search = search[:search.index("&list=")]
            #If the bot isnt already playing something, extract info and download the new video
            if not self.PLAYERS['0'].is_playing():     
                await ctx.send("`Searching ...`")
                #Options for extracting data from the video
                ydl_opts = {
                    'default_search': 'auto', 'format': 'bestaudio/best',
                    'outtmpl': 'audio/%(title)s-%(id)s.opus',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'opus',
                        'preferredquality': '192',
                    }]
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    result = ydl.extract_info("ytsearch:"+search) #Search for a video and then extract the info
                    if 'entries' in result:
                        try:
                            video = result['entries'][0]
                        except:
                            video = result
                    else:
                        video = result
                    #Download the video
                    ydl.download([video['webpage_url']])
                
                #Gets the name of the audio file
                outfile = ydl.prepare_filename(video)

                #posts the video url in the chat
                await ctx.send(video['webpage_url'])

                #plays the audio to the voice channel if it isn't already playing
                self.PLAYERS['0'].play(discord.FFmpegPCMAudio(outfile))
            else:
                await ctx.send("I am already playing a file!")
                return()
        else:
            await ctx.send("You have to be in a voice channel dumby")


    #Checks to see if the user is valid to run the commands below
    def voiceChecker(self, ctx):
        author = ctx.message.author 
        try:
            #If the user is in the voice channel
            if author.voice.channel == self.PLAYERS['0'].channel:
                return(True) #return True
            else:
                return(False)
        except AttributeError:
            return(False)


    #Stops the audio
    @commands.command(pass_context = True)
    async def stop(self, ctx):
        if self.voiceChecker(ctx) == True: #If the user is in the voice channel
            if self.PLAYERS['0'].is_playing(): #And the bot is playing something
                await ctx.send("`Stopping ...`") 
                self.PLAYERS['0'].stop() #Stop the player
            else:
                await ctx.send("I am not playing anything right now!")
        else: 
            await ctx.send("You have to be in my voice channel dipshit")
            return()

    #leaves the voice channel if it is connected to a voice channel
    @commands.command(pass_context = True)
    async def leave(self, ctx):
        if self.voiceChecker(ctx) == True: #If the user is in the voice channel
            if self.PLAYERS['0'].is_connected(): #and the bot is in a voice channel
                await ctx.send("`Goodbye`")
                self.PLAYERS['0'].stop() #Stop 
                await self.PLAYERS['0'].disconnect() #Leave
                self.PLAYERS['0'] = None #Reset the voice player objects
            else:
                #if the bot is not in the voice channel, let the user know
                await ctx.send("I am not connected to a voice channel right now!")
                return()
        else:
            #Prevents a user from making the bot leave when they are not connected 
            await ctx.send("You are either not in my voice channel or not connected at all.")
            return()
        
    #pauses the video if it is playing something
    @commands.command()
    async def pause(self, ctx):
        if self.voiceChecker(ctx) == True: #If the user is in the voice channel
            if self.PLAYERS['0'].is_playing(): #and if the bot is playing
                await ctx.send("`Pausing ...`")
                self.PLAYERS['0'].pause() #Pause
            else:
                await ctx.send("I am not playing anything right now!")
        else:
            #Prevents the user from pausing if they are not in the voice channel
            await ctx.send("You are either not in my voice channel or not connected at all.")

    #resumes the video if it is paused
    @commands.command()
    async def resume(self, ctx):
        if self.voiceChecker(ctx) == True: #If the user is in the voice channel
            if self.PLAYERS['0'].is_paused(): #and the audio is paused
                await ctx.send("`Resuming ...`")
                self.PLAYERS['0'].resume() #Resume
            else:
                await ctx.send("I am not paused!") #Let the user know that the bot is not paused
        else:
            #Prevent the user from resuming if not in the voice channel
            await ctx.send ("You are either not in my voice channel or not connected at all.")

def setup(bot):
    bot.add_cog(Audio(bot))
