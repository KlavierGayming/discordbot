# "Simple" multi-functional discord bot with slash commands
- Contains music, moderation and fun features.
- Slightly configurable without editing the main python file
- Modular with cogs which are auto-detected and auto-loaded if set up properly.

To run this bot, you will need `discord.py`, `ytdl-patched` and `ffmpeg` and `nest_asyncio` packages. Install them through pip.<br>
You will also need to create a `token.json` file with the contents being:<br>
```json
{ 
    "token": "your bot token",
    "prefix": "prefix",
    "playing_status": "whatever the hell you want."
}
```

To add a new cog with new commands, add a new `.py` file to the `cogs/` folder. The file must have an async def called setup which loads the cog.<br>
For example:
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