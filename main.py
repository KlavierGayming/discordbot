#i have no idea what im doing.

import discord
from stuff.youtubestuff import YTDLSource
from discord.ext import commands
import json
from yt_dlp import YoutubeDL as ytdl
from stuff.sessioning import ServerSession
from typing import Dict
import asyncio
import json
import os
import nest_asyncio
import stuff.customHelp as ch
intents = discord.Intents.all()
nest_asyncio.apply()

tokenjson = {}
with open("token.json") as token:
    tokenjson = json.loads(token.read())

bot = commands.Bot(command_prefix=tokenjson["prefix"], case_insensitive=True, intents=intents, description="Joe mama.", help_command=ch.HelpCommand())



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
