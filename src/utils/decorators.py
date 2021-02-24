import discord
from discord.ext import commands
from src.utils.classes import GameUser
from src.utils.embeds import make_text_embed
from src.utils.colors import RED


def require_join():
    async def predicate(ctx):
        if GameUser.exist_user(ctx.bot.con, str(ctx.author.id)):
            return True
        else:
            await ctx.reply(embed=make_text_embed(ctx.author, "가입이 필요한 커맨드입니다.", RED))
            return False

    return commands.check(predicate)
