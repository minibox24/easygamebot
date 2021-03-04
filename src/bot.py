import discord
from discord.ext import commands
from src.utils import get_config
from src.utils.database import connect_database, init_stock


class EasyGameBot(commands.Bot):
    def __init__(self):
        config = get_config()
        intents = discord.Intents.all()
        super().__init__(command_prefix=config["bot"]["prefix"], intents=intents)
        self.config = config

        self.con = connect_database(self.config["database"]["path"])

    async def on_ready(self):
        self.remove_command("help")
        await self.change_presence(activity=discord.Game(self.config["bot"]["status"]))
        self.allowed_mentions = discord.AllowedMentions(
            replied_user=self.config["bot"]["reply_mention"]
        )

        init_stock(
            self.con,
            self.config["game"]["stock"]["stocks"],
            self.config["game"]["stock"]["stock_default_price"],
        )

        for extension in get_config()["bot"]["extensions"]:
            self.load_extension(extension)

        print("준비 완료!")

    async def on_message(self, message):
        await self.process_commands(message)
