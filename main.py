#i have no idea what im doing.

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

intents = discord.Intents.all()

tokenjson = {}
with open("token.json") as token:
    tokenjson = json.loads(token.read())

bot = commands.Bot(command_prefix=tokenjson["prefix"], case_insensitive=True, intents=intents, description="Joe mama.")

@bot.event
async def on_ready():
    print("Logged in as " + str(bot.user))

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command()
async def join(ctx):
    """Joins a voice channel"""
    voice = ctx.author.voice
    if voice is None:
        return await ctx.send("You have to be in a VC!")

    await voice.channel.connect()
    if ctx.voice_client.is_connected():
        server_sessions[ctx.guild.id] = ServerSession(ctx.guild.id, ctx.voice_client)
        return await ctx.send("Connected successfully")
    else:
        return await ctx.send("Failed to connect!")

@bot.command()
async def leave(ctx):
    channel = ctx.voice_client
    if ctx.guild.id in server_sessions:
        await channel.disconnect()
        channel.cleanup()
        del server_sessions[ctx.guild.id]
        await ctx.send("Disconnected.")

@bot.command()
async def play(ctx, *, url):
    voice = ctx.author.voice
    if ctx.voice_client == None:
            if voice is None:
                return await ctx.send("You have to be in a VC!")

            await voice.channel.connect()
            if ctx.voice_client.is_connected():
                server_sessions[ctx.guild.id] = ServerSession(ctx.guild.id, ctx.voice_client)
            else:
                return await ctx.send("Failed to connect!")
    if ctx.guild.id in server_sessions and ctx.voice_client.channel != voice.channel:
        await ctx.voice_client.move_to(voice.channel)
    if ctx.voice_client.is_playing() != True and ctx.voice_client.is_paused() != True:
        async with ctx.typing():
            player = await YTDLSource.play(url=url, loop=bot.loop, stream=True)
            await server_sessions[ctx.guild.id].add_to_queue(ctx, url, bot)
            ctx.voice_client.play(player, after=lambda e=None: weenus(ctx, e))
        await ctx.send("**Now playing:** `"+ str(player.title) + "`\n" + str(player.yturl))
    else:
        await server_sessions[ctx.guild.id].add_to_queue(ctx, url, bot)

def weenus(ctx, e):
    func = asyncio.run_coroutine_threadsafe(server_sessions[ctx.guild.id].after_playing(ctx, e, bot), bot.loop)
    time.sleep(4)
    func.result()

@bot.command()
async def queue(ctx):
    if ctx.guild.id in server_sessions:
        await ctx.send(server_sessions[ctx.guild.id].display_queue())
    else:
        await ctx.send("There is no queue to display!")

@bot.command()
async def stop(ctx):
    if ctx.voice_client.is_playing() == True and ctx.guild.id in server_sessions:
        ctx.voice_client.stop()
        await ctx.send("Stopped playing.")
    else:
        await ctx.send("You have to be playing to stop!")

@bot.command()
async def pause(ctx):
    if ctx.voice_client.is_playing() == True and ctx.voice_client.is_paused() == False and ctx.guild.id in server_sessions:
        ctx.voice_client.pause()
        await ctx.send("Paused.")
    else:
        await ctx.send("You have to be playing/not paused!")

@bot.command()
async def resume(ctx):
    if ctx.voice_client.is_playing() == False and ctx.voice_client.is_paused() == True and ctx.guild.id in server_sessions:
        ctx.voice_client.resume()
        await ctx.send("Resumed.")
    else:
        await ctx.send("You have to be paused/playing!")

@bot.command()
async def skip(ctx):
    guildid = ctx.guild.id
    if guildid in server_sessions:
        session = server_sessions[guildid]
        vc = session.vc
        if vc.is_playing():
            if len(session.queue) > 1:
                vc.stop()

@bot.command()
async def remove(ctx, i: int):
    guildid = ctx.guild.id
    if guildid in server_sessions:
        if i==0:
            await ctx.send("Cannot remove current playing song, please use skip command instead.")
        elif i >= len(server_sessions[guildid].queue):
            await ctx.send(f"The queue is not that long, there are only {len(server_sessions[guildid].queue)-1} items.")
        else:
            removedname= server_sessions[guildid].queue[i].title
            server_sessions[guildid].queue.pop(i)
            await ctx.send(f"Removed `{removedname}` from queue.")

@bot.command()
async def clear(ctx):
    guildid = ctx.guild.id
    if guildid in server_sessions:
        voice_client = server_sessions[guildid].vc
        server_sessions[guildid].queue = []
        if voice_client.is_playing():
            voice_client.stop()
        await ctx.send("Queue cleared and current song stopped.")

@bot.command()
async def song(ctx):
    """Show the current song"""
    guild_id = ctx.guild.id
    if guild_id in server_sessions:
        await ctx.send(f'**Now playing:** `{server_sessions[guild_id].queue[0].title}`')
    else:
        await ctx.send("Not playing anything right now!")

@bot.command()
async def quote(ctx):
    contents = ""
    with open("quotes.json") as q:
        contents = q.read()
    data = json.loads(contents)
    currEntry = random.randint(0, len(data))
    
    await ctx.send("`" + data[currEntry]["text"] + "`" + "\n\-  " + data[currEntry]["author"])

@bot.command()
async def say(ctx, text):
    if ctx.author.id == 419934381084246036:
        async with ctx.typing():    
            await ctx.message.delete()
            await ctx.send(text)

#sessioning bullshit!!
server_sessions: Dict[int, ServerSession] = {} 



token = tokenjson["token"]

bot.run(token)