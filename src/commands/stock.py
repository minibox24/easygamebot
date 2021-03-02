import discord
from discord.ext import commands, tasks

from src.utils import (
    colors,
    stock_next_price,
    format_money,
    seconds_to_timestr,
    make_graph,
    one_more_check,
)
from src.utils.database import get_stock_info
from src.utils.classes import GameUser
from src.utils.embeds import make_text_embed
from src.utils.decorators import require_join

from typing import List
from random import randint
from sqlite3 import Cursor
from json import dumps, loads
from time import time, strftime, localtime
from datetime import datetime


class Stock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stock_change_loop.change_interval(
            seconds=bot.config["game"]["stock"]["stock_change_time"]
        )
        self.stock_change_loop.start()

    def cog_unload(self):
        self.stock_change_loop.cancel()

    @tasks.loop(seconds=30.0)
    async def stock_change_loop(self):
        cur: Cursor = self.bot.con.cursor()
        stocks: List[str] = self.bot.config["game"]["stock"]["stocks"]

        for stock in stocks:
            data = get_stock_info(self.bot.con, stock)

            cap = randint(data["cap"] - 5000, data["cap"] + 5000)
            cap = randint(150, 50000) if cap < 150 else cap  # 최소 금액
            cap = randint(100000, 150000) if cap > 150000 else cap  # 최대금액

            cur.execute("SELECT stock FROM users")
            price = stock_next_price(
                cap, list(map(lambda x, n=stock: len(loads(x[0])[n]), cur.fetchall()))
            )

            timestr = strftime("%H:%M:%S", localtime(time()))

            for i in data["history"][:]:
                if i["time"] == timestr:
                    data["history"].remove(i)

            data["history"].append({"time": timestr, "price": price})

            if len(data["history"]) > 100:
                del data["history"][0]

            cur.execute(
                "UPDATE stocks SET price=?, cap=?, history=? WHERE name=?",
                (
                    str(price),
                    str(cap),
                    dumps(data["history"], ensure_ascii=False),
                    stock,
                ),
            )

        self.bot.con.commit()

    @commands.group("주식")
    async def stock(self, ctx: commands.Context):
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
    async def stock_info(self, ctx: commands.Context, name: str = None):
        data = {}
        stocks: List[str] = self.bot.config["game"]["stock"]["stocks"]

        for stock in stocks:
            data[stock] = get_stock_info(self.bot.con, stock)

        if data.get(name):
            history = list(data[name]["history"])

            if len(history) > 20:
                for i, _ in enumerate(history):
                    if i % 5 != 0:
                        history[i]["time"] = "​" * i

            x = list(map(lambda o: o["time"], history))
            y = list(map(lambda o: o["price"], history))

            buf = make_graph(x, y)
            dynamic = ""
            unit = self.bot.config["game"]["unit"]
            price = data[name]["price"]

            if GameUser.exist_user(self.bot.con, str(ctx.author.id)):
                user = GameUser(self.bot.con, str(ctx.author.id))
                shares = len(user.stock[name])
                if shares != 0:
                    avg = sum(user.stock[name]) / shares
                    pal = int(price - avg)
                    times = round(price / avg, 2)
                    dynamic = f"{shares}주 보유 중\n"
                    dynamic += f"손익: {format_money(pal, unit)} ( {times}x )\n"
                    dynamic += f"가진 {shares}주를 전부 팔면 {format_money(shares * price, unit)}을(를) 얻습니다"

            embed = make_text_embed(
                ctx.author,
                f"**주가: {format_money(price, unit)}**\n{dynamic}",
                title=name,
            )
            embed.set_image(url="attachment://graph.png")

            return await ctx.reply(
                embed=embed, file=discord.File(buf, filename="graph.png")
            )

        next_time = seconds_to_timestr(
            (
                self.stock_change_loop.next_iteration.replace(tzinfo=None)
                - datetime.utcnow()
            ).seconds
        )

        unit = self.bot.config["game"]["unit"]
        chart = []

        for i in data:
            price = data[i]["price"]
            if len(data[i]["history"]) >= 2:
                status = data[i]["history"][-2]["price"] < data[i]["price"]
                value = abs(data[i]["price"] - data[i]["history"][-2]["price"])
                chart.append(
                    f"{'+' if status else '-'} {i} {format_money(price, unit)} ( {'▲' if status else '▼'} {value} )"
                )
            else:
                chart.append(f"? {i} {format_money(price, unit)}")

        chart = "\n".join(chart)
        await ctx.reply(
            embed=make_text_embed(
                ctx.author,
                f"**주식 차트**\n```diff\n{chart}\n```\n`{next_time} 후 가격 변동`",
            )
        )

    @stock.command("매수")
    @require_join()
    async def stock_buy(self, ctx: commands.Context, name: str, shares: int = None):
        if shares and shares < 1:
            return await ctx.reply(
                embed=make_text_embed(ctx.author, "1주 이상부터 구매할수 있습니다.", colors.RED)
            )

        try:
            data = get_stock_info(self.bot.con, name)
        except NameError:
            return await ctx.reply(
                embed=make_text_embed(
                    ctx.author, f"찾을 수 없는 주식 `{name}` 입니다.", colors.RED
                )
            )

        user = GameUser(self.bot.con, str(ctx.author.id))

        if not shares:
            shares = user.money // data["price"]

            if not shares:
                return await ctx.reply(
                    embed=make_text_embed(
                        ctx.author,
                        f"보유하고 있는 돈으로는 `{name}` 의 주식을 1주도 구매할 수 없습니다.",
                        colors.RED,
                    )
                )

        price = data["price"] * shares
        unit = self.bot.config["game"]["unit"]

        if user.money < price:
            more = format_money(price - user.money, unit)
            return await ctx.reply(
                embed=make_text_embed(
                    ctx.author,
                    f"`{name}` 의 주식을 {shares}주 구매하려면 {more}이(가) 더 필요합니다.",
                    colors.RED,
                )
            )

        buy, message = await one_more_check(
            ctx, f"`{name}` 의 주식 {shares}주를 {format_money(price, unit)}으로 구매할까요?"
        )

        if not buy:
            return await message.edit(
                embed=make_text_embed(
                    ctx.author,
                    "구매를 취소했습니다.",
                    colors.ORANGE,
                )
            )

        user.money -= price
        for i in range(shares):
            user.stock[name].append(data["price"])
        user.commit()

        return await message.edit(
            embed=make_text_embed(
                ctx.author,
                f"`{name}` 의 주식을 {format_money(price, unit)}으로 {shares}주 구매했습니다.\n"
                f"현재 보유 금액: {format_money(user.money, unit)}",
            )
        )

    @stock.command("매도")
    @require_join()
    async def stock_sell(self, ctx: commands.Context, name: str, shares: int = None):
        if shares and shares < 1:
            return await ctx.reply(
                embed=make_text_embed(ctx.author, "1주 이상부터 판매할수 있습니다.", colors.RED)
            )

        try:
            data = get_stock_info(self.bot.con, name)
        except NameError:
            return await ctx.reply(
                embed=make_text_embed(
                    ctx.author, f"찾을 수 없는 주식 `{name}` 입니다.", colors.RED
                )
            )

        user = GameUser(self.bot.con, str(ctx.author.id))

        if not shares:
            shares = len(user.stock[name])

            if not shares:
                return await ctx.reply(
                    embed=make_text_embed(
                        ctx.author,
                        f"보유하고 있는 `{name}` 의 주식이 없습니다.",
                        colors.RED,
                    )
                )

        price = data["price"] * shares
        unit = self.bot.config["game"]["unit"]

        if len(user.stock[name]) < shares:
            more = shares - len(user.stock[name])
            return await ctx.reply(
                embed=make_text_embed(
                    ctx.author,
                    f"`{name}` 의 주식을 {shares}주 판매하려면 {more}주가 더 필요합니다.",
                    colors.RED,
                )
            )

        buy, message = await one_more_check(
            ctx, f"`{name}` 의 주식 {shares}주를 {format_money(price, unit)}으로 판매할까요?"
        )

        if not buy:
            return await message.edit(
                embed=make_text_embed(
                    ctx.author,
                    "판매를 취소했습니다.",
                    colors.ORANGE,
                )
            )

        user.money += price
        for i in range(shares):
            del user.stock[name][0]
        user.commit()

        return await message.edit(
            embed=make_text_embed(
                ctx.author,
                f"`{name}` 의 주식을 {shares}주 판매해 {format_money(price, unit)}을(를) 얻었습니다.\n"
                f"현재 보유 금액: {format_money(user.money, unit)}",
            )
        )


def setup(bot):
    bot.add_cog(Stock(bot))
