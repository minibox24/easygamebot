import discord
from discord.ext import commands

from src.utils import emoji_check, make_text_embed
from src.utils.colors import RED, YELLOW, ORANGE

import traceback


class Default(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, err: Exception):
        ignored = (commands.CommandNotFound,)
        if isinstance(err, ignored):
            return
        elif isinstance(err, commands.CheckFailure):
            await ctx.message.add_reaction("⛔")
            if await emoji_check("⛔", ctx):
                await ctx.reply(embed=make_text_embed(ctx.author, "권한이 부족합니다.", RED))
        elif isinstance(err, commands.CommandOnCooldown):
            await ctx.message.add_reaction("🕒")
            if await emoji_check("🕒", ctx):
                await ctx.reply(
                    embed=make_text_embed(
                        ctx.author,
                        f"쿨다운 중 입니다. {round(err.retry_after, 2)}초 후 다시 시도해 주세요.",
                        ORANGE,
                    )
                )
        else:
            await ctx.message.add_reaction("⚠")
            if await emoji_check("⚠", ctx):
                tb = traceback.format_exception(type(err), err, err.__traceback__)
                err = [line.rstrip() for line in tb]
                errstr = "\n".join(err)
                print(errstr)

                if len(errstr) > 512:
                    errstr = "...\n\n" + errstr[512:]

                await ctx.reply(
                    embed=make_text_embed(
                        ctx.author,
                        f"**커맨드 실행 중 오류가 발생했습니다.**\n```py\n{errstr}```",
                        YELLOW,
                    )
                )


def setup(bot):
    bot.add_cog(Default(bot))
