# Simple (currently music-centered) discord bot with queueing.
Idk what else to say here. It's like literally what i just told you.
**This is kinda *bo***ring
idk what else to put here actually
spent like 3 days making this

Also to run this, you will need `discord.py`, `ytdl-patched` and `ffmpeg` and `nest_asyncio` packages. Install them through pip.
To run this bot, you will need to create a `token.json` file with the contents being:
```json
{ 
    "token": "your bot token",
    "prefix": "prefix"
}
```

This bot uses cogs. They're automatically detected in the `cogs/` folder. If you want to add new functions, add a new `.py` file to the `cogs/` folder. The file must have an async def called setup which loads the cog.
ex.
```python
from discord.ext import commands
class mycog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def ping(self, ctx):
        ctx.send("Ping!")
    
async def setup(bot):
    await bot.add_cog(mycog(bot))
```