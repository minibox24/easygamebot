import discord
from discord.ext import commands
from src.utils import get_config, connect_database


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

        for extension in get_config()["bot"]["extensions"]:
            self.load_extension(extension)
        print("준비 완료!")

    async def on_message(self, message):
        await self.process_commands(message)
