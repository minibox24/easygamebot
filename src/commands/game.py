import discord
from discord.ext import commands

from src.utils.classes import GameUser
from src.utils.embeds import make_text_embed
from src.utils.decorators import require_join

from typing import Dict


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown: Dict[int, float] = {}

    @commands.command("일", aliases=["ㅇ"])
    @require_join()
    async def work(self, ctx: commands.Context):
        user = GameUser(self.bot.con, str(ctx.author.id))
        # TODO: work command


def setup(bot):
    bot.add_cog(Game(bot))
