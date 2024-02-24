import shutil

import discord
from discord.ext import commands

from config import CONFIG
from localisation import localise


class Debug(commands.Cog, name="debug"):
    author = "googer_'s blood and tears :sob:"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def init_on_ready(self):
        pass

    cmds = discord.SlashCommandGroup(
        "debug",
        "",
        name_localizations=localise("cog.debug.command_group.name"),
        description_localizations=localise("cog.debug.command_group.desc"),
    )

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.debug.commands.senddbs.name"),
        description_localizations=localise("cog.debug.commands.senddbs.desc"),
    )
    @commands.is_owner()
    async def senddbs(self, ctx: discord.ApplicationContext):
        shutil.make_archive("temp/__TEMP_DEBUG_SENDDBS", "zip", "databases")
        with open("temp/__TEMP_DEBUG_SENDDBS.zip", "rb") as file:
            await ctx.respond(
                localise("cog.debug.answers.senddbs.ok", ctx.interaction.locale),
                ephemeral=True,
                file=discord.File(file, filename="databases.zip"),
            )


def setup(bot):
    bot.add_cog(Debug(bot))
