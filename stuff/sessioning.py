import discord
from discord.ext import commands
from typing import Dict, List
from stuff.youtubestuff import YTDLSource
import asyncio
import time

class Source:
    def __init__(self, audio_source, metadata):
        self.audio_source: discord.AudioSource = audio_source
        self.url: str = metadata.get("webpage_url", "unknown url")
        self.title: str = metadata.get('title', "uknown title")
        self.metadata = metadata
        pass

class ServerSession:
    def __init__(self, guildid, vc):
        self.guildid: int = guildid
        self.vc: discord.VoiceClient = vc
        self.queue: List[Source] = []
    def display_queue(self) -> str:
        if self.queue:
            curqueue = []
            for i in self.queue:
                curqueue.append(i.title)
            notplaying = ""
            s = 0
            while s < len(curqueue):
                notplaying+=f"{s}, `{curqueue[s]}`\n"
                s+=1
            return "**Currently Playing**: " + notplaying
        else:
            return "Queue is empty!"
    
    async def add_to_queue(self, ctx, url, bot):
        yt_source = await YTDLSource.play(url, loop=bot.loop, stream=True)
        self.queue.append(yt_source)
        if self.vc.is_playing():
            async with ctx.typing():
                vurl = await YTDLSource.geturl(url)
                await ctx.send(f'**Added to queue:** `{yt_source.title}`\n{vurl}')
            pass
    async def after_playing(self, ctx, e, bot: commands.bot):
        error = e
        if error:
            raise error
        else:
            if self.queue:
                self.queue.pop(0)
                await self.play_next(ctx, bot)
    async def play_next(self, ctx, bot: commands.bot):
        if self.queue:
            async with ctx.typing():
                player = await YTDLSource.play(self.queue[0].url, loop=bot.loop, stream=True)
                vurl = await YTDLSource.geturl(self.queue[0].url)
                self.vc.play(player, after=lambda e=None: self.weenus(ctx, e, bot))
            await ctx.send(f"**Now playing**: `{self.queue[0].title}`\n{vurl}")
    def weenus(self, ctx, e, bot: commands.bot):
        func = asyncio.run_coroutine_threadsafe(self.after_playing(ctx, e, bot), bot.loop)
        try:
            time.sleep(4)
            func.result()
        except Exception as e:
            print(e)
            pass


    