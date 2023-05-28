import discord
from discord.ext import commands
import json
import random

class Basics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def quote(self, ctx):
        """Returns a random quote"""
        contents = ""
        with open("quotes.json") as q:
            contents = q.read()
        data = json.loads(contents)
        currEntry = random.randint(0, len(data))
        
        await ctx.send("`" + data[currEntry]["text"] + "`" + "\n\-  " + data[currEntry]["author"])


async def setup(bot):
    await bot.add_cog(Basics(bot))