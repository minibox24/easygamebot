from sanic import Blueprint
from sanic.response import json as resjson
from discord.ext import commands

from src.utils import get_config
from src.utils.classes import Status

import asyncio

api = Blueprint("api", url_prefix="/api")


def response(status: Status, message: str = "", data=None) -> resjson:
    if data is None:
        data = {}
    return resjson({"status": status.value, "message": message, "data": data})


@api.route("/")
async def main(req):
    bot: commands.Bot = req.app.bot
    print(bot.is_ready(), req.app.bf.done())
    return response(Status.OK, "Hello, World!")


@api.route("/on")
async def bot_on(req):
    config = get_config()
    bot: commands.Bot = req.app.bot
    req.app.BotFuture = asyncio.ensure_future(bot.start(config["bot"]["token"]))
    return response(Status.OK, "bot on")


@api.route("/off")
async def bot_off(req):
    future: asyncio.Future = req.app.BotFuture
    future.cancel()
    return response(Status.OK, "bot off")
