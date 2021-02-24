import discord
from discord.ext import commands


class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("hello")
    async def hello(self, ctx):
        await ctx.send("hello")


def setup(bot):
    bot.add_cog(Default(bot))
