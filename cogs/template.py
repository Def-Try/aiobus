import discord
from discord.ext import commands
from config import CONFIG
from localisation import LOCALISATIONS
import json

class template(commands.Cog):
    author = "googer_"

    def __init__(self, bot):
        self.bot = bot

    cmds = discord.SlashCommandGroup("", "",
        name_localizations=LOCALISATIONS["cog"]["template"]["command_group"]["name"],
        description_localizations=LOCALISATIONS["cog"]["template"]["command_group"]["desc"])
    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["template"]["commands"]["cmd"]["name"],
        description_localizations=LOCALISATIONS["cog"]["template"]["commands"]["cmd"]["desc"])
    def cmd(self, ctx: discord.ApplicationContext):
        await ctx.reply("template")

def setup(bot):
    bot.add_cog(template(bot))
