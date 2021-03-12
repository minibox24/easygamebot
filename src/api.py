from sanic import Blueprint
from sanic.response import json as resjson
from discord.ext import commands

from src.utils import get_config
from src.utils.classes import Status

import asyncio
from functools import wraps
from base64 import b64decode
import binascii


api = Blueprint("api", url_prefix="/api")
username = "admin"


def response(
    status: Status, message: str = "", data=None, status_code: int = 200
) -> resjson:
    if data is None:
        data = {}
    return resjson(
        {"status": status.value, "message": message, "data": data}, status=status_code
    )


def authorized():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_auth = False

            try:
                typ, cre = request.headers.get("Authorization").split()

                config = get_config()
                if typ == "Basic":
                    if (
                        b64decode(cre.encode()).decode()
                        == f'{username}:{config["admin_tool"]["password"]}'
                    ):
                        is_auth = True
            except binascii.Error:
                pass
            except ValueError:
                pass
            except AttributeError:
                pass
            if is_auth:
                res = await f(request, *args, **kwargs)
                return res
            else:
                return response(Status.AUTH, "need authorization", status_code=401)

        return decorated_function

    return decorator


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
