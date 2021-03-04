import discord
from discord.ext import commands

from src.utils import make_text_embed, format_money, colors, one_more_check
from src.utils.classes import Item, Items, GameUser


class Store(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command("상점")
    async def item_store(self, ctx: commands.Context, *, name: str = None):
        unit = self.bot.config["game"]["unit"]
        if name:
            item = Item.get(name)

            if not item:
                return await ctx.reply(
                    embed=make_text_embed(
                        ctx.author, f"{name}은(는) 찾을 수 없는 아이템입니다.", colors.RED
                    )
                )

            color = colors.GREEN

            if GameUser.exist_user(self.bot.con, str(ctx.author.id)):
                user = GameUser(self.bot.con, str(ctx.author.id))
                if user.money < item.price:
                    color = colors.RED

            return await ctx.reply(
                embed=make_text_embed(
                    ctx.author,
                    f"**{item.name}**\n{format_money(item.price, unit)}\n```\n{item.description}\n```",
                    color,
                )
            )
        await ctx.reply(
            embed=make_text_embed(
                ctx.author,
                "\n".join(
                    map(
                        lambda i: f"{i.name}: {format_money(i.price, unit)}",
                        Items,
                    )
                ),
                title="아이템 상점",
            )
        )

    @commands.command("구매")
    async def item_buy(self, ctx: commands.Context, *, name: str):
        item = Item.get(name)

        if not item:
            return await ctx.reply(
                embed=make_text_embed(
                    ctx.author, f"{name}은(는) 찾을 수 없는 아이템입니다.", colors.RED
                )
            )

        user = GameUser(self.bot.con, str(ctx.author.id))
        unit = self.bot.config["game"]["unit"]

        if item in user.items:
            return await ctx.reply(
                embed=make_text_embed(
                    ctx.author,
                    f"이미 {name}을(를) 보유중입니다.",
                    colors.RED,
                )
            )

        if user.money < item.price:
            more = format_money(item.price - user.money, unit)
            return await ctx.reply(
                embed=make_text_embed(
                    ctx.author,
                    f"{name}을(를) 구매하려면 {more}이(가) 더 필요합니다.",
                    colors.RED,
                )
            )

        buy, message = await one_more_check(
            ctx, f"{name}을(를) {format_money(item.price, unit)}(으)로 구매할까요?"
        )

        if not buy:
            return await message.edit(
                embed=make_text_embed(
                    ctx.author,
                    "구매를 취소했습니다.",
                    colors.ORANGE,
                )
            )

        user.money -= item.price
        user.items.append(item)
        user.commit()

        return await message.edit(
            embed=make_text_embed(
                ctx.author,
                f"{name}을(를) {format_money(item.price, unit)}(으)로 구매했습니다.\n"
                f"현재 보유 금액: {format_money(user.money, unit)}",
            )
        )


def setup(bot):
    bot.add_cog(Store(bot))
