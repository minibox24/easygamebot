from sanic import Blueprint
from sanic.response import json as response_json
import discord
from discord.ext import commands

from src.utils import get_config
from src.utils.classes import Status

import asyncio
import json


api = Blueprint("api", url_prefix="/api")


def response(status: Status, message: str = "", data=None, typ="response") -> str:
    if data is None:
        data = {}
    return json.dumps(
        {"typ": typ, "status": status.value, "message": message, "data": data},
        ensure_ascii=False,
    )


def check_auth(pw):
    config = get_config()
    return pw == config["admin_tool"]["password"]


@api.route("/")
async def api_main(req):
    return response_json({"message": "Hello, World!"})


async def api_status(app):
    try:
        future: asyncio.Future = app.BotFuture
        bot: commands.Bot = app.bot
    except AttributeError:
        return response(Status.OK, data={"status": False})

    done = future.done()
    ready = bot.is_ready()

    return response(Status.OK, data={"status": not done and ready})


async def api_bot_start(app):
    config = get_config()
    bot: commands.Bot = app.bot
    app.BotFuture = asyncio.ensure_future(bot.start(config["bot"]["token"]))
    return response(Status.OK, "bot on")


async def api_bot_stop(app):
    future: asyncio.Future = app.BotFuture

    future.cancel()
    return response(Status.OK, "bot off")


async def api_bot_restart(app):
    future: asyncio.Future = app.BotFuture
    bot: commands.Bot = app.bot
    config = get_config()

    future.cancel()
    app.BotFuture = asyncio.ensure_future(bot.start(config["bot"]["token"]))
    return response(Status.OK, "bot off")


async def api_auth(r):
    pass


@api.websocket("/ws")
async def socket(request, ws):
    routes = {
        "auth": api_auth,
        "status": api_status,
        "start": api_bot_start,
        "stop": api_bot_stop,
        "restart": api_bot_restart,
    }
    need_auth = ["start", "stop", "restart"]

    while True:
        # request data: { route: '', data: {}, password(Optional): '' }
        req = await ws.resv()
        req = json.loads(req)

        route = req.get("route")
        data = req.get("data")
        password = req.get("password")

        if not route or not isinstance(data, dict):
            await ws.send(
                response(Status.ERROR, "데이터 형식이 올바르지 않습니다.", {"code": "INVALID_DATA"})
            )
            continue

        if not routes.get(req["route"]):
            await ws.send(
                response(Status.ERROR, "존재하지 않는 라우트입니다.", {"code": "NOT_FOUND_ROUTE"})
            )
            continue

        auth = check_auth(password)

        if route in need_auth and not auth:
            await ws.send(
                response(Status.ERROR, "인증이 필요한 라우트입니다.", {"code": "NEED_AUTH"})
            )
            continue

        func = routes[route]
        await ws.send(func(request.app))
