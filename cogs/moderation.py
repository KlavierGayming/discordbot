from discord.ext import commands
import discord
import asyncio
import datetime

class Moderation(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        """Ban a user."""
        if ctx.author.top_role > member.top_role:
            await member.ban(reason=reason)
            await ctx.send("Successfully banned member" + member.mention)
        else:
            await ctx.author.send("Your role isn't high enough to ban this member!")

    @commands.hybrid_command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, * , reason):
        """Kick a user"""
        if ctx.author.top_role > member.top_role:
            await ctx.guild.kick(member, reason=reason)
            await ctx.send(f"Successfully kicked {member.mention}")
        else:
            await ctx.send("Your role isn't high enough to ban this member!")
    
    @commands.hybrid_command(aliases=["unban"])
    @commands.has_permissions(ban_members = True)
    async def pardon(self, ctx,*, member: str):
        """Unban a user. Doesn't support discriminators as of now, unban those manually."""
        converter = commands.UserConverter()
        try:
            users: discord.User = await converter.convert(ctx=ctx, argument=member)
        except:
            users: discord.User = None

        if users == None:
            await ctx.reply("Please enter a valid member!")

        else:
            guild = ctx.guild
            await ctx.reply(f"Successfully unbanned **{users}**")
            await guild.unban(user=users)
        
    @commands.hybrid_command(usage="timeout <member> <duration in hours with h behind> <duration in minutes with m behind>", aliases=["mute"])
    @commands.has_permissions(kick_members=True)
    async def timeout(self, ctx, member:discord.Member, durationh, durationm):
        """Time out a user."""
        if ctx.author.top_role > member.top_role:
            await member.timeout(datetime.timedelta(days=0, hours=int(durationh[:-1]), minutes=int(durationm[:-1])))
            await ctx.send(f"Timed out {member.mention} succesfully for {durationh} {durationm}")
        
async def setup(bot):
    await bot.add_cog(Moderation(bot))