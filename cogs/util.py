import discord
from discord.ext import commands
from typing import Dict
import json

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command()
    async def link(self, ctx, *, name: str):
        """Returns link from link database"""
        async with ctx.typing():
            with open("cogs/db.json") as f:
                jsonThing = f.read()
            db: Dict = json.loads(jsonThing)
            savedIndex: int = None
            for i in range(len(db["linknames"])):
                if db["linknames"][i].lower() == name.lower():
                    savedIndex = i
        if savedIndex is not None:
            actualStuff = f"{name}:\n{db['linkvalues'][savedIndex]}"
        else:
            actualStuff = "Couldn't find " + name + " in link database!"
        await ctx.send(actualStuff)

async def setup(bot):
    await bot.add_cog(Util(bot))