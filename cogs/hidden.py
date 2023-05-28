import discord
from discord.ext import commands

class Hidden(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, text):
        if ctx.author.id == 419934381084246036:
            async with ctx.typing():    
                await ctx.message.delete()
                await ctx.send(text)

async def setup(bot):
    await bot.add_cog(Hidden(bot))