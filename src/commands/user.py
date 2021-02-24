import discord
from discord.ext import commands

from src.utils import colors
from src.utils.classes import GameUser
from src.utils.embeds import make_text_embed
from src.utils.decorators import require_join


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("가입")
    async def join_user(self, ctx):
        if GameUser.exist_user(self.bot.con, str(ctx.author.id)):
            return await ctx.reply(
                embed=make_text_embed(
                    ctx.author,
                    f"{ctx.author.name}님은 이미 {self.bot.config['game']['name']} 서비스에 가입하셨습니다.",
                    colors.RED,
                )
            )

        GameUser.join(self.bot.con, str(ctx.author.id))
        await ctx.reply(
            embed=make_text_embed(
                ctx.author,
                f"{ctx.author.name}님은 {self.bot.config['game']['name']} 서비스에 가입하셨습니다.",
            )
        )

    @commands.command("탈퇴")
    @require_join()
    async def remove_user(self, ctx):
        user = GameUser(self.bot.con, str(ctx.author.id))
        user.remove()
        await ctx.reply(
            embed=make_text_embed(
                ctx.author,
                f"{ctx.author.name}님은 {self.bot.config['game']['name']} 서비스에서 탈퇴하셨습니다.",
                colors.RED,
            )
        )

    @commands.command("정보")
    async def info_user(self, ctx, target: discord.User = None):
        if not target:
            if not GameUser.exist_user(ctx.bot.con, str(ctx.author.id)):
                return await ctx.reply(
                    embed=make_text_embed(ctx.author, "가입이 필요한 커맨드입니다.", colors.RED)
                )
            target = ctx.author

        user = GameUser(self.bot.con, str(target.id))
        await ctx.reply(
            embed=make_text_embed(
                ctx.author, f"{target.name}: {user.money}원 보유 중", colors.AQUA
            )
        )


def setup(bot):
    bot.add_cog(User(bot))
