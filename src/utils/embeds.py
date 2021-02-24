import discord
from src.utils.colors import GREEN


def make_text_embed(user: discord.User, text: str, color: int = GREEN) -> discord.Embed:
    embed = discord.Embed(color=color)
    embed.description = text
    embed.set_footer(text=user.display_name, icon_url=user.avatar_url)
    return embed
