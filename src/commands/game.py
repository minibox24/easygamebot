import discord
from discord.ext import commands

from src.utils import format_money, seconds_to_timestr
from src.utils.classes import GameUser, ItemEffect
from src.utils.embeds import make_text_embed
from src.utils.decorators import require_join

from typing import Dict
from time import time
from random import randint


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown: Dict[int, float] = {}

    @commands.command("일", aliases=["ㅇ"])
    @require_join()
    async def work(self, ctx: commands.Context):
        user = GameUser(self.bot.con, str(ctx.author.id))

        cooltime = 5
        for item in list(user.items):
            effect: ItemEffect = item.effect
            if effect.name == "work-speed":
                if cooltime > effect.effect:
                    cooltime = effect.effect
                if effect.use_remove:
                    user.items.remove(item)
                    user.commit()

        if (
            self.cooldown.get(ctx.author.id)
            and time() - self.cooldown[ctx.author.id] < cooltime
        ):
            raise commands.CommandOnCooldown(
                commands.Cooldown(1, cooltime, commands.BucketType.user),
                cooltime - (time() - self.cooldown[ctx.author.id]),
            )

        x, y = map(int, self.bot.config["game"]["work_money"].split("-"))

        for item in list(user.items):
            effect: ItemEffect = item.effect
            if effect.name == "work-power":
                if y > effect.effect:
                    y *= int(effect.effect)
                if effect.use_remove:
                    user.items.remove(item)
                    user.commit()

        add = randint(x, y)
        user.money += add
        user.commit()

        self.cooldown[ctx.author.id] = time()

        await ctx.reply(
            embed=make_text_embed(
                ctx.author,
                f"당신을 일을 해서 {format_money(add, self.bot.config['game']['unit'])}을(를) 얻었습니다."
                f"\n다음 일은 {seconds_to_timestr(cooltime)}후에 가능합니다.",
            )
        )


def setup(bot):
    bot.add_cog(Game(bot))
