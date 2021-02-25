import discord
from discord.ext import commands

from src.utils import colors
from src.utils.classes import GameUser
from src.utils.embeds import make_text_embed
from src.utils.decorators import require_join


class Stock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group("주식")
    async def stock(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.reply(
                embed=make_text_embed(
                    ctx.author,
                    f"{ctx.prefix}주식 정보 (주식 이름)\n"
                    f"{ctx.prefix}주식 매수 [주식 이름] [주]\n"
                    f"{ctx.prefix}주식 매도 [주식 이름] [주]\n\n"
                    f"`[]` 필수 `()` 선택",
                    colors.ORANGE,
                )
            )

    @stock.command("정보")
    async def stock_info(self, ctx, name: str = None):
        if name:
            return


def setup(bot):
    bot.add_cog(Stock(bot))
