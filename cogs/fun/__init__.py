import asyncio
import io
import random

import discord
from discord.ext import commands

from . import languages
from config import CONFIG
from localisation import DEFAULT_LOCALE
from localisation import localise


class Fun(commands.Cog):
    author = "googer_"

    def __init__(self, bot):
        self.bot = bot
        self.injected = []

    def inject(self, class_):
        self.injected.append(class_(self.bot, self.cmds))

    @commands.Cog.listener("on_ready")
    async def init_on_ready(self):
        pass

    cmds = discord.SlashCommandGroup(
        "fun",
        "",
        name_localizations=localise("cog.fun.command_group.name"),
        description_localizations=localise("cog.fun.command_group.desc"),
    )

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.fun.commands.crash_server.name"),
        description_localizations=localise("cog.fun.commands.crash_server.desc"),
    )
    async def crash_server(self, ctx: discord.ApplicationContext):
        msg = await ctx.respond(
            localise(
                "cog.fun.answers.crash_server.progress", ctx.interaction.locale
            ).format(percent=0)
        )
        await asyncio.sleep(0.5)
        done = 1
        while done < 85:
            done += random.randint(5, 10)
            await asyncio.sleep(random.randint(1, 5) / 10)
            await msg.edit_original_response(
                content=localise(
                    "cog.fun.answers.crash_server.progress", ctx.interaction.locale
                ).format(percent=done)
            )
        await asyncio.sleep(5)
        await msg.edit_original_response(
            content=localise(
                "cog.fun.answers.crash_server.error", ctx.interaction.locale
            )
        )

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.fun.commands.translate.name"),
        description_localizations=localise("cog.fun.commands.translate.desc"),
    )
    async def translate(
        self,
        ctx: discord.ApplicationContext,
        mode: discord.Option(
            str,
            name_localizations=localise("cog.fun.commands.translate.options.mode.name"),
            description=localise(
                "cog.fun.commands.translate.options.mode.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.fun.commands.translate.options.mode.desc"
            ),
            choices=["to", "from"],
        ),
        language: discord.Option(
            str,
            name_localizations=localise(
                "cog.fun.commands.translate.options.language.name"
            ),
            description=localise(
                "cog.fun.commands.translate.options.language.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.fun.commands.translate.options.language.desc"
            ),
            choices=list(languages.languages.keys()),
        ),
        text: discord.Option(
            str,
            name_localizations=localise("cog.fun.commands.translate.options.text.name"),
            description=localise(
                "cog.fun.commands.translate.options.text.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.fun.commands.translate.options.text.desc"
            ),
        ),
    ):
        translated = languages.languages[language].translate(mode, text)
        # pylint: disable=broad-exception-caught
        try:
            await ctx.respond(
                localise(
                    "cog.fun.answers.translate.done.text", ctx.interaction.locale
                ).format(
                    text=text,
                    language=language,
                    translated=translated,
                    way=localise(
                        f"cog.fun.answers.translate.{mode}", ctx.interaction.locale
                    ),
                ),
                ephemeral=True,
            )
        except Exception:
            f = io.StringIO(translated)
            await ctx.respond(
                localise(
                    "cog.fun.answers.translate.done.file", ctx.interaction.locale
                ).format(
                    text=text,
                    language=language,
                    way=localise(
                        f"cog.fun.answers.translate.{mode}", ctx.interaction.locale
                    ),
                ),
                ephemeral=True,
                file=discord.File(f),
            )
            f.close()
        # pylint: enable=broad-exception-caught

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.fun.commands.parse_rpd.name"),
        description_localizations=localise("cog.fun.commands.parse_rpd.desc"),
    )
    async def parse_rpd(
        self,
        ctx: discord.ApplicationContext,
        text: discord.Option(
            str,
            name_localizations=localise("cog.fun.commands.parse_rpd.options.text.name"),
            description=localise(
                "cog.fun.commands.parse_rpd.options.text.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.fun.commands.parse_rpd.options.text.desc"
            ),
        ),
    ):
        rtext = text
        radio = False
        radio_channel = ""
        radio_channel_done = False
        text = ""
        doing_text = True
        action = ""
        doing_action = False
        for n, ch in enumerate(rtext):
            if ch == ";" and n == 0:
                radio, radio_channel = True, "common"
                radio_channel_done = True
                continue
            if ch == ":" and n == 0:
                radio = True
                continue
            if radio and not radio_channel_done:
                if ch == " ":
                    radio_channel_done = True
                    continue
                radio_channel += ch
                continue
            if radio and ch == "*":
                action = text
                text = ""
                doing_text = True
                continue
            if ch == "*" and text:
                action = text
                text = ""
                doing_text = True
                continue
            if ch == "*" and not text:
                doing_action = True
                doing_text = False
                continue
            if doing_action:
                action += ch
            if doing_text:
                text += ch
        if text and text[-1] not in ".!?":
            text += "."

        def sliceindex(x):
            i = 0
            for c in x:
                if c.isalpha():
                    i = i + 1
                    return i
                i = i + 1
            return i

        def upperfirst(x):
            i = sliceindex(x)
            return x[:i].upper() + x[i:]

        text = upperfirst(text.strip())
        name = (
            ctx.author.display_name
            if ctx.author.display_name
            else ctx.author.name if not ctx.author.nick else ctx.author.nick
        )
        ending = (
            "no"
            if not text
            else "ask" if text[-1] == "?" else "exclaim" if text[-1] == "!" else "say"
        )
        await ctx.respond(
            localise(
                "cog.fun.answers.parse_rpd."
                + ending
                + "."
                + ("w" if radio else "n")
                + "radio."
                + ("w" if action else "n")
                + "act",
                ctx.interaction.locale,
            ).format(
                nick=name, text=text, action=action, channel=upperfirst(radio_channel)
            )
        )


def setup(bot):
    bot.add_cog(Fun(bot))
