from sanic import Blueprint
from sanic.response import json as resjson
from discord.ext import commands

from src.utils.classes import Status

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
