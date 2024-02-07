import discord
from discord.ext import commands
from localisation import localise
from config import CONFIG


class GoogerIsLenivy(commands.Cog):
    author = "googer_"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_msg(self, message):
        if 891289716501119016 in [u.id for u in message.mentions]:
            await message.reply("лень")


def setup(bot):
    bot.add_cog(GoogerIsLenivy(bot))
