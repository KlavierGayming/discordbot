#i have no idea what im doing.
#nvm i kinda do

import discord
from discord.ext import commands
import json
from typing import Dict
import asyncio
import json
import os
import nest_asyncio
import stuff.customHelp as ch
import logging
from discord import app_commands

intents = discord.Intents.all()
nest_asyncio.apply()

tokenjson = {}
with open("token.json") as token:
    tokenjson = json.loads(token.read())
bot = commands.Bot(command_prefix=tokenjson["prefix"], case_insensitive=True, intents=intents, description="A random bot", help_command=ch.HelpCommand(), tree_cls=app_commands.tree.CommandTree)
bot.activity = discord.Game(name=tokenjson["playing_status"])



@bot.event
async def on_ready():
    print("Logged in as " + str(bot.user))
    try: 
        await bot.tree.sync()
        print("Synced")
    except Exception as e:
        print(e)


#@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Pass in all arguments, please.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You're missing permissions to run this command.")
    else:
        await ctx.send("Internal error. Please report to bot developer @klavg.")
        print(error)


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
