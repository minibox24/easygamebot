from src.bot import EasyGameBot
from src.webserver import app
from src.utils import get_config
from sanic.websocket import WebSocketProtocol
import asyncio


if __name__ == "__main__":
    config = get_config()
    bot = EasyGameBot()
    app.bot = bot

    loop = asyncio.get_event_loop()

    BotFuture = asyncio.ensure_future(bot.start(config["bot"]["token"]))
    app.BotFuture = BotFuture
    Webfuture = asyncio.ensure_future(
        app.create_server(
            host=config["admin_tool"]["host"],
            port=config["admin_tool"]["port"],
            return_asyncio_server=True,
            protocol=WebSocketProtocol,
            access_log=False,
        )
    )

    loop.run_forever()
