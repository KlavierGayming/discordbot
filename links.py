#ok so

import discord
from discord.ext import commands
import json

class Links(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def link(self, ctx, name: str):
        
        with open("db.json") as f:
            g=f.read()
        dbJson = json.loads(g)
        dbJson["linkNames"][0] = "lol"
        with open("db.json") as f:
            g2=f.write(json.dumps(dbJson))
        await ctx.send(json.loads(g2))


async def setup(bot: commands.Bot):
    await bot.add_cog(Links)