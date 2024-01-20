import discord
from discord.ext import commands
from config import CONFIG
from localisation import LOCALISATIONS
import json


class template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    cmds = discord.SlashCommandGroup("", "",
                                     name_localizations=LOCALISATIONS["cog"]["template"]["command_group"]["name"],
                                     description_localisations=LOCALISATIONS["cog"]["template"]["command_group"]["desc"])

    @cmds.command(guild_ids=CONFIG["g_ids"],
                  name_localizations=LOCALISATIONS["cog"]["template"]["commands"]["cmd"]["name"],
                  description_localisations=LOCALISATIONS["cog"]["template"]["commands"]["cmd"]["desc"])
def setup(bot):
    bot.add_cog(template(bot))
