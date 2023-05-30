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
            await ctx.send("Successfully banned member" + member)
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
    
    @commands.hybrid_command()
    @commands.has_permissions(ban_members = True)
    async def pardon(self, ctx,*, member: discord.User):
        """Unban a user."""
        if member == None:
            embed = discord.Embed(f"{ctx.message.author}, Please enter a valid member!")
            await ctx.reply(embed=embed)

        else:
            guild = ctx.guild
            await ctx.send(f"Successfully unbanned **{member}**")
            await guild.unban(user=member)
        
    @commands.hybrid_command(usage="Joe, timeout <member> <duration in hours with h behind> <duration in minutes with m behind>", aliases=["mute"])
    @commands.has_permissions(kick_members=True)
    async def timeout(self, ctx, member:discord.Member, durationh, durationm):
        """Time out a user."""
        if ctx.author.top_role > member.top_role:
            await member.timeout(datetime.timedelta(days=0, hours=int(durationh[:-1]), minutes=int(durationm[:-1])))
            await ctx.send(f"Timed out {member.mention} succesfully for {durationh} {durationm}")
        
async def setup(bot):
    await bot.add_cog(Moderation(bot))