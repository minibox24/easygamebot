from sanic import Blueprint, websocket
from sanic.response import json as response_json
import discord
from discord.ext import commands

from typing import Optional
from src.utils import get_config, get_com_info
from src.utils.classes import Status

import asyncio
import json


api = Blueprint("api", url_prefix="/api")
client: Optional[websocket.WebSocketConnection] = None


def response(
    status: Status = Status.OK,
    message: str = "",
    data: Optional[dict] = None,
    typ="response",
) -> str:
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


async def api_status(app, _):
    bot: commands.Bot = app.bot

    try:
        future: asyncio.Future = app.bot_future
    except AttributeError:
        return response(data={"status": False})

    done = future.done()
    ready = bot.is_ready()

    return response(data={"status": not done and ready})


async def api_bot_start(app, _):
    config = get_config()
    bot: commands.Bot = app.bot
    app.bot_future = asyncio.ensure_future(bot.start(config["bot"]["token"]))
    return response(message="bot start")


async def api_bot_stop(app, _):
    future: asyncio.Future = app.bot_future

    future.cancel()
    return response(message="bot stop")


async def api_bot_restart(app, _):
    future: asyncio.Future = app.bot_future
    bot: commands.Bot = app.bot
    config = get_config()

    future.cancel()
    app.bot_future = asyncio.ensure_future(bot.start(config["bot"]["token"]))
    return response(message="bot restart")


async def api_auth(_, data):
    return response(data={"auth": check_auth(data.get("password"))})


async def api_setup(app, _):
    bot: commands.Bot = app.bot
    config = get_config()

    discord_info = (
        {
            "avatar": str(bot.user.avatar_url_as("png")),
            "name": bot.user.name,
            "tag": bot.user.discriminator,
        }
        if bot.user
        else {"avatar": "", "name": "Bot", "tag": "0000"}
    )

    return response(
        data={
            "status": False,
            "servers": "-",
            "users": [],
            "discord": discord_info,
            "com": get_com_info(),
            "config": config,
        }
    )


async def api_setting(app, data):
    pass


@api.websocket("/ws")
async def socket(request, ws):
    routes = {
        "auth": api_auth,
        "status": api_status,
        "start": api_bot_start,
        "stop": api_bot_stop,
        "restart": api_bot_restart,
        "setup": api_setup,
        "setting": api_setting,
    }
    need_auth = ["start", "stop", "restart", "setup", "setting"]

    global client
    client = ws

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
        await ws.send(func(request.app, data))
