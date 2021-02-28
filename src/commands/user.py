import discord
from discord.ext import commands

from src.utils import colors, timestamp_to_timestr, seconds_to_timestr, format_money
from src.utils.classes import GameUser
from src.utils.embeds import make_text_embed
from src.utils.decorators import require_join

import time


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("가입")
    async def join_user(self, ctx: commands.Context):
        if GameUser.exist_user(self.bot.con, str(ctx.author.id)):
            return await ctx.reply(
                embed=make_text_embed(
                    ctx.author,
                    f"{ctx.author.name}님은 이미 {self.bot.config['game']['name']} 서비스에 가입하셨습니다.",
                    colors.RED,
                )
            )

        user = GameUser.join(
            self.bot.con,
            str(ctx.author.id),
            gift=self.bot.config["game"]["register_money"],
        )

        for i in self.bot.config["game"]["stock"]["stocks"]:
            user.stock[i] = []
        user.commit()

        await ctx.reply(
            embed=make_text_embed(
                ctx.author,
                f"{ctx.author.name}님은 {self.bot.config['game']['name']} 서비스에 가입하셨습니다.",
            )
        )

    @commands.command("탈퇴")
    @require_join()
    async def remove_user(self, ctx: commands.Context):
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
    async def info_user(self, ctx: commands.Context, target: discord.User = None):
        if not target:
            if not GameUser.exist_user(ctx.bot.con, str(ctx.author.id)):
                return await ctx.reply(
                    embed=make_text_embed(ctx.author, "가입이 필요한 커맨드입니다.", colors.RED)
                )
            target = ctx.author

        user = GameUser(self.bot.con, str(target.id))
        embed = make_text_embed(
            ctx.author,
            f"{seconds_to_timestr(int(time.time() - user.join_time))} 전 가입"
            if time.time() - user.join_time < 21600
            else f"{timestamp_to_timestr(user.join_time)} 가입",
            colors.AQUA,
        )

        embed.add_field(
            name="돈", value=format_money(user.money, self.bot.config["game"]["unit"])
        )
        embed.add_field(
            name="주식",
            value="\n".join(map(lambda x: f"{x}: {len(user.stock[x])}주", user.stock)),
        )
        embed.set_author(name=target.name, icon_url=target.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command("출석체크", aliases=["출첵", "ㅊㅊ"])
    @require_join()
    async def check_user(self, ctx: commands.Context):
        user = GameUser(self.bot.con, str(ctx.author.id))

        check_money = self.bot.config["game"]["check_money"]
        check_time = self.bot.config["game"]["check_time"]
        unit = self.bot.config["game"]["unit"]

        if time.time() - user.check_time < check_time:
            return await ctx.reply(
                embed=make_text_embed(
                    ctx.author,
                    f"{seconds_to_timestr(check_time - int(time.time() - user.check_time))}후에 다시 출석체크가 가능합니다.",
                    colors.RED,
                )
            )

        user.money += check_money
        user.check_time = time.time()
        user.commit()

        return await ctx.reply(
            embed=make_text_embed(
                ctx.author,
                f"출석체크 완료! {format_money(check_money, unit)}을(를) 얻었습니다.\n"
                f"현재 돈: {format_money(user.money, unit)}\n\n"
                f"{seconds_to_timestr(check_time)}후에 다시 출석체크가 가능합니다.",
                colors.GREEN,
            )
        )


def setup(bot):
    bot.add_cog(User(bot))
