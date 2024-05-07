import urllib.parse

import aiohttp
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
    async def googleforyou(
        self,
        ctx: discord.ApplicationContext,
        question: discord.Option(
            str,
            name_localizations=localise(
                "cog.util.commands.googlethatforyou.options.question.name"
            ),
            description=localise(
                "cog.util.commands.googlethatforyou.options.question.desc",
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
                "cog.util.commands.googlethatforyou.options.asker.desc", DEFAULT_LOCALE
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

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.util.commands.translate.name"),
        description_localizations=localise("cog.util.commands.translate.desc"),
    )
    async def translate(
        self,
        ctx: discord.ApplicationContext,
        text: discord.Option(
            str,
            name_localizations=localise(
                "cog.util.commands.translate.options.text.name"
            ),
            description=localise(
                "cog.util.commands.translate.options.text.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.util.commands.translate.options.text.desc"
            ),
        ),
        target: discord.Option(
            str,
            name_localizations=localise(
                "cog.util.commands.translate.options.target.name"
            ),
            description=localise(
                "cog.util.commands.translate.options.target.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.util.commands.translate.options.target.desc"
            ),
        ) = None,
        source: discord.Option(
            str,
            name_localizations=localise(
                "cog.util.commands.translate.options.source.name"
            ),
            description=localise(
                "cog.util.commands.translate.options.source.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.util.commands.translate.options.source.desc"
            ),
        ) = "auto",
    ):
        if target is None:
            target = ctx.interaction.locale
        await ctx.response.defer()
        data = {}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://clients5.google.com/translate_a/t",
                    timeout=5,
                    params={
                        "client": "dict-chrome-ex",
                        "dt": "t",
                        "tl": target,
                        "sl": source,
                        "q": text,
                    },
                ) as response:
                    data = await response.json()
        except TimeoutError:
            await ctx.followup.send(
                localise("cog.util.answers.translate.error", ctx.interaction.locale)
            )
            return
        except Exception:
            await ctx.followup.send(
                localise("cog.util.answers.translate.error", ctx.interaction.locale)
            )
            return
        await ctx.followup.send(
            localise(
                "cog.util.answers.translate.translated", ctx.interaction.locale
            ).format(target=target, source=data[0][1], translated=data[0][0]),
            allowed_mentions=discord.AllowedMentions.none()
        )


def setup(bot):
    bot.add_cog(Utils(bot))
