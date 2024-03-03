import urllib.parse

import discord
from discord.ext import commands

from config import CONFIG
from localisation import DEFAULT_LOCALE
from localisation import localise


class Utils(commands.Cog, name="util"):
    author = "googer_"

    def __init__(self, bot):
        self.bot = bot

    cmds = discord.SlashCommandGroup(
        "util",
        "",
        name_localizations=localise("cog.util.command_group.name"),
        description_localizations=localise("cog.util.command_group.desc"),
    )

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.util.commands.googlethatforyou.name"),
        description_localizations=localise("cog.util.commands.googlethatforyou.desc"),
    )
    async def cmd(
        self,
        ctx: discord.ApplicationContext,
        question: discord.Option(
            str,
            name_localizations=localise(
                "cog.util.commands.googlethatforyou.options.question.name"
            ),
            description=localise(
                "cog.util.commands.fgooglethatforyou.options.question.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.util.commands.googlethatforyou.options.question.desc"
            ),
        ),
        asker: discord.Option(
            discord.abc.User,
            name_localizations=localise(
                "cog.util.commands.googlethatforyou.options.asker.name"
            ),
            description=localise(
                "cog.util.commands.fgooglethatforyou.options.asker.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.util.commands.googlethatforyou.options.asker.desc"
            ),
        ) = None,
    ):
        question = urllib.parse.quote(question, safe="")
        if asker is None:
            await ctx.respond(
                localise(
                    "cog.util.answers.googlethatforyou.noasker", ctx.interaction.locale
                ).format(link=f"https://googlethatforyou.com/?q={question}")
            )
            return
        await ctx.respond(
            localise(
                "cog.util.answers.googlethatforyou.wasker", ctx.interaction.locale
            ).format(
                link=f"https://googlethatforyou.com/?q={question}", asker=asker.mention
            )
        )


def setup(bot):
    bot.add_cog(Utils(bot))
