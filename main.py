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
from cogs import music
import os
import logging
import nest_asyncio

intents = discord.Intents.all()
nest_asyncio.apply()

tokenjson = {}
with open("token.json") as token:
    tokenjson = json.loads(token.read())

bot = commands.Bot(command_prefix=tokenjson["prefix"], case_insensitive=True, intents=intents, description="Joe mama.")

class Basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def quote(self, ctx):
        contents = ""
        with open("quotes.json") as q:
            contents = q.read()
        data = json.loads(contents)
        currEntry = random.randint(0, len(data))
        
        await ctx.send("`" + data[currEntry]["text"] + "`" + "\n\-  " + data[currEntry]["author"])

    @commands.command()
    async def say(self, ctx, text):
        if ctx.author.id == 419934381084246036:
            async with ctx.typing():    
                await ctx.message.delete()
                await ctx.send(text)

@bot.event
async def on_ready():
    print("Logged in as " + str(bot.user))

token = tokenjson["token"]
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
async def fuckthisshit():
    await load()
    #await bot.run(token, log_handler=logging.StreamHandler(), log_level=logging.DEBUG)
    bot.run(token)

asyncio.run(fuckthisshit())
