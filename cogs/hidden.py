import discord
from discord.ext import commands
import json
from typing import Dict

class Hidden(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("token.json") as f:
            jsonData = f.read()
        self.tokenJson = json.loads(jsonData)

    @commands.command()
    async def say(self, ctx, text):
        if ctx.author.id == self.tokenJson["bot_owner"]:
            async with ctx.typing():    
                await ctx.message.delete()
                await ctx.send(text)
    
    @commands.command()
    async def addLink(self, ctx, name: str, value: str):
        if ctx.author.id == self.tokenJson["bot_owner"]:
            with open("cogs/db.json") as f:
                g=f.read()
            dbJson: Dict = json.loads(g)
            dbJson["linknames"].append(name)
            dbJson["linkvalues"].append(value)
            with open("cogs/db.json", "r+") as f:
                g2=f.write(json.dumps(dbJson))
            await ctx.send("Successfully added link " + name)
async def setup(bot):
    await bot.add_cog(Hidden(bot))