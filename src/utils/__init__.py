import asyncio
from typing import Dict, List, Tuple, Any
import discord
from discord.ext import commands

from json import load
from datetime import datetime
from math import log, sqrt
import matplotlib.pyplot as plt
from io import BytesIO
from os import getpid
from psutil import cpu_percent, virtual_memory

from src.utils import colors
from src.utils.embeds import make_text_embed


def get_config() -> Dict[str, Any]:
    with open("./config.json", encoding="utf-8") as f:
        return load(f)


def timestamp_to_timestr(timestamp: float) -> str:
    dt = datetime.fromtimestamp(timestamp)
    ampm = "오전" if dt.hour < 12 else "오후"
    hour = dt.hour if dt.hour <= 12 else dt.hour - 12
    return f"{dt.year}년 {dt.month}월 {dt.day}일 {ampm} {hour}시 {dt.minute}분 {dt.second}초"


def seconds_to_timestr(second: int) -> str:
    h = 0
    m = 0

    if second >= 3600:
        h = second // 3600
        second -= h * 3600

    if second >= 60:
        m = second // 60
        second -= m * 60

    timelist = []
    if h != 0:
        timelist.append(f"{h}시간")
    if m != 0:
        timelist.append(f"{m}분")
    if second != 0:
        timelist.append(f"{second}초")
    if h == 0 and m == 0 and second == 0:
        return "0초"

    return " ".join(timelist)


def format_money(money: int, unit: str) -> str:
    return f"{format(money, ',')}{unit}"


def stock_next_price(cap: int, shares: List[int]) -> int:
    log11 = log(1.1)
    sq = 0

    for share in shares:
        if share < 1:
            continue
        sq += log(cap * share) / log11

    return int(cap * (1 / (1 - (sqrt(sq) / cap))))


def make_graph(x: List[int], y: List[int]) -> BytesIO:
    plt.clf()
    plt.figure(figsize=(10, 5))
    ax = plt.subplot(1, 1, 1)
    plt.plot(x, y, color="r")
    if len(list(filter(lambda o: "​" not in o, x))) >= 10:
        for label in ax.xaxis.get_ticklabels():
            label.set_rotation(30)
    buf = BytesIO()
    plt.savefig(buf)
    buf.seek(0)
    return buf


async def one_more_check(
    ctx: commands.Context, text: str
) -> Tuple[bool, discord.Message]:
    message: discord.Message = await ctx.reply(
        embed=make_text_embed(ctx.author, text, colors.AQUA)
    )

    await message.add_reaction("✅")
    await message.add_reaction("❎")

    try:
        reaction, _ = await ctx.bot.wait_for(
            "reaction_add",
            check=lambda r, u: r.message.id == message.id and u == ctx.author,
            timeout=60.0,
        )
        return reaction.emoji == "✅", message
    except asyncio.TimeoutError:
        return False, message


async def emoji_check(emoji: str, ctx: commands.Context) -> bool:
    try:
        reaction, _ = await ctx.bot.wait_for(
            "reaction_add",
            check=lambda r, u: r.message.id == ctx.message.id and u == ctx.author,
            timeout=60.0,
        )
        return reaction.emoji == emoji
    except asyncio.TimeoutError:
        return False


def get_com_info() -> dict:
    tot, ava = virtual_memory()[:2]
    return {
        "cpu": f"{round(cpu_percent())}%",
        "ram": f"{round(ava / 1e9, 1)}GB / {round(tot / 1e9, 1)}GB",
        "pid": getpid(),
    }
