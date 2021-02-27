import discord
from discord.ext import commands, tasks

from src.utils import (
    colors,
    stock_next_price,
    format_money,
    seconds_to_timestr,
    make_graph,
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
            seconds=bot.config["game"]["stock_change_time"]
        )
        self.stock_change_loop.start()

    def cog_unload(self):
        self.stock_change_loop.cancel()

    @tasks.loop(seconds=30.0)
    async def stock_change_loop(self):
        cur: Cursor = self.bot.con.cursor()
        stocks: List[str] = self.bot.config["game"]["stocks"]

        for stock in stocks:
            data = get_stock_info(self.bot.con, stock)

            cap = randint(data["cap"] - 5000, data["cap"] + 5000)
            cap = randint(300, 50000) if cap < 300 else cap  # 최소 금액
            cap = randint(250000, 300000) if cap > 300000 else cap  # 최대금액

            cur.execute("SELECT stock FROM users")
            price = stock_next_price(
                cap, list(map(lambda x: loads(x[0])[stock]["shares"], cur.fetchall()))
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
        data = {}
        stocks: List[str] = self.bot.config["game"]["stocks"]

        for stock in stocks:
            data[stock] = get_stock_info(self.bot.con, stock)

        if data.get(name):
            history = list(data[name]["history"])

            for i in range(len(history)):
                if i % 5 != 0:
                    history[i]["time"] = "​" * i

            x = list(map(lambda o: o["time"], history))
            y = list(map(lambda o: o["price"], history))

            buf = make_graph(x, y)

            embed = make_text_embed(
                ctx.author,
                format_money(data[name]["price"], self.bot.config["game"]["unit"]),
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
            status = data[i]["history"][-2]["price"] < data[i]["price"]
            chart.append(
                f"{'+' if status else '-'} {i} {format_money(price, unit)} ( {'▲' if status else '▼'} {abs(data[i]['price'] - data[i]['history'][-2]['price'])} )"
            )

        chart = "\n".join(chart)
        await ctx.reply(
            embed=make_text_embed(
                ctx.author,
                f"**주식 차트**\n```diff\n{chart}\n```\n`{next_time} 후 가격 변동`",
            )
        )


def setup(bot):
    bot.add_cog(Stock(bot))
