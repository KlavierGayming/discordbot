import discord
from stuff.youtubestuff import YTDLSource
from discord.ext import commands
import random
import json
from yt_dlp import YoutubeDL as ytdl
from stuff.sessioning import ServerSession
from typing import Dict
import time
import asyncio
import json

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #session bullshit
        self.server_sessions: Dict[int, ServerSession] = {} 
    
    @commands.hybrid_command()
    async def join(self, ctx):
        """Joins a voice channel"""
        voice = ctx.author.voice
        if voice is None:
            return await ctx.send("You have to be in a VC!")

        await voice.channel.connect()
        if ctx.voice_client.is_connected():
            self.server_sessions[ctx.guild.id] = ServerSession(ctx.guild.id, ctx.voice_client, self.bot)
            return await ctx.send("Connected successfully")
        else:
            return await ctx.send("Failed to connect!")
    
    @commands.hybrid_command()
    async def leave(self, ctx):
        """Leave voice channel"""
        channel = ctx.voice_client
        if ctx.guild.id in self.server_sessions:
            await channel.disconnect()
            channel.cleanup()
            del self.server_sessions[ctx.guild.id]
            await ctx.send("Disconnected.")

    def weenus(self, ctx, e):
        func = asyncio.run_coroutine_threadsafe(self.server_sessions[ctx.guild.id].after_playing(ctx, e, commands), self.bot.loop)
        time.sleep(4)
        func.result()

        
    @commands.hybrid_command()
    async def play(self, ctx, *, query):
        """Play song (from YT URL or YT search query)"""
        voice = ctx.author.voice
        if ctx.voice_client == None:
                if voice is None:
                    return await ctx.send("You have to be in a VC!")

                await voice.channel.connect()
                if ctx.voice_client.is_connected():
                    self.server_sessions[ctx.guild.id] = ServerSession(ctx.guild.id, ctx.voice_client, self.bot)
                else:
                    return await ctx.send("Failed to connect!")
        if ctx.guild.id in self.server_sessions and ctx.voice_client.channel != voice.channel:
            await ctx.voice_client.move_to(voice.channel)
        if ctx.voice_client.is_playing() != True and ctx.voice_client.is_paused() != True:
            async with ctx.typing():
                player = await YTDLSource.play(url=query, loop=self.bot.loop, stream=True)
                await self.server_sessions[ctx.guild.id].add_to_queue(ctx, query)
                ctx.voice_client.play(player, after=lambda e=None: self.weenus(ctx, e))
            await ctx.send("**Now playing:** `"+ str(player.title) + "`\n" + str(player.yturl))
        else:
            async with ctx.typing():
                await self.addtoqueue(ctx, query)
    
    async def addtoqueue(self, ctx, query):
        await self.server_sessions[ctx.guild.id].add_to_queue(ctx, query)
        session = self.server_sessions[ctx.guild.id]
        newinqueue = session.queue[len(session.queue)-1]
        print("shiz")
        if self.server_sessions[ctx.guild.id].vc.is_playing():    
            await ctx.send(f"Added to queue: {newinqueue.title}\n{newinqueue.yturl}")
    @commands.hybrid_command()
    async def queue(self, ctx):
        """Show current queue"""
        if ctx.guild.id in self.server_sessions:
            await ctx.send(self.server_sessions[ctx.guild.id].display_queue())
        else:
            await ctx.send("There is no queue to display!")

    @commands.hybrid_command()
    async def stop(self, ctx):
        """Stop player"""
        if ctx.voice_client.is_playing() == True and ctx.guild.id in self.server_sessions:
            ctx.voice_client.stop()
            self.server_sessions[ctx.guild.id].queue = []
            await ctx.send("Stopped playing.")
        else:
            await ctx.send("You have to be playing to stop!")

    @commands.hybrid_command()
    async def pause(self, ctx):
        """Pause playing song"""
        if ctx.voice_client.is_playing() == True and ctx.voice_client.is_paused() == False and ctx.guild.id in self.server_sessions:
            ctx.voice_client.pause()
            await ctx.send("Paused.")
        else:
            await ctx.send("You have to be playing/not paused!")
    
    @commands.hybrid_command()
    async def resume(self, ctx):
        """Resumes paused song"""
        if ctx.voice_client.is_playing() == False and ctx.voice_client.is_paused() == True and ctx.guild.id in self.server_sessions:
            ctx.voice_client.resume()
            await ctx.send("Resumed.")
        else:
            await ctx.send("You have to be paused/playing!")

    @commands.hybrid_command()
    async def skip(self, ctx):
        """Skip current song in queue"""
        guildid = ctx.guild.id
        if guildid in self.server_sessions:
            session = self.server_sessions[guildid]
            vc = session.vc
            if vc.is_playing():
                if len(session.queue) > 1:
                    if session.songloop:
                        session.queue.pop(0)
                    vc.stop()
                    await ctx.send("Skipping!")

    @commands.hybrid_command()
    async def remove(self, ctx, numberinqueue: int):
        """Remove Indexed Item from queue"""
        guildid = ctx.guild.id
        if guildid in self.server_sessions:
            if numberinqueue==0:
                await ctx.send("Cannot remove current playing song, please use skip command instead.")
            elif numberinqueue >= len(self.server_sessions[guildid].queue):
                await ctx.send(f"The queue is not that long, there are only {len(self.server_sessions[guildid].queue)-1} items.")
            else:
                removedname= self.server_sessions[guildid].queue[numberinqueue].title
                self.server_sessions[guildid].queue.pop(numberinqueue)
                await ctx.send(f"Removed `{removedname}` from queue.")

    @commands.hybrid_command()
    async def clear(self, ctx):
        """Clear the queue"""
        guildid = ctx.guild.id
        if guildid in self.server_sessions:
            voice_client = self.server_sessions[guildid].vc
            self.server_sessions[guildid].queue = []
            if voice_client.is_playing():
                voice_client.stop()
            await ctx.send("Queue cleared and current song stopped.")

    @commands.hybrid_command()
    async def loop(self, ctx):
        """Toggle looping the current song"""
        guildid = ctx.guild.id
        if guildid in self.server_sessions:
            self.server_sessions[guildid].songloop = not self.server_sessions[guildid].songloop
            songloop = self.server_sessions[guildid].songloop
            loopstr = ""
            if songloop: loopstr = "Looping"
            else: loopstr = "Stopped looping"
            await ctx.send(f"{loopstr} current song/next song that plays.")
        else:
            await ctx.send("I need to be connected to a VC to do that!")

    @commands.hybrid_command()
    async def song(self, ctx):
        """Show the current song"""
        guild_id = ctx.guild.id
        if guild_id in self.server_sessions and len(self.server_sessions[guild_id].queue) >=1:
            await ctx.send(f'**Now playing:** `{self.server_sessions[guild_id].queue[0].title}`')
        else:
            await ctx.send("Not playing anything right now!")
    
async def setup(bot: commands.bot):
    await bot.add_cog(Music(bot))