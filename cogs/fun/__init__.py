import discord
from discord.ext import commands
from localisation import localise, DEFAULT_LOCALE
from config import CONFIG

import asyncio
import random

from . import languages

28356
1331
46827
12104

class fun(commands.Cog):
    author = "googer_"

    def __init__(self, bot):
        self.bot = bot
        self.injected = []

    def inject(self, class_):
        self.injected.append(class_(self.bot, self.cmds))

    @commands.Cog.listener("on_ready")
    async def init_on_ready(self):
        pass

    cmds = discord.SlashCommandGroup("fun", "",
        name_localizations=localise("cog.fun.command_group.name"),
        description_localizations=localise("cog.fun.command_group.desc"))

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.fun.commands.crash_server.name"),
        description_localizations=localise("cog.fun.commands.crash_server.desc"))
    async def crash_server(self, ctx: discord.ApplicationContext):
        msg = await ctx.respond(localise("cog.fun.answers.crash_server.progress", ctx.interaction.locale).format(percent=0))
        await asyncio.sleep(0.5)
        done = 1
        while done < 85:
            done += random.randint(5, 10)
            await asyncio.sleep(random.randint(1, 5) / 10)
            await msg.edit_original_response(content=localise("cog.fun.answers.crash_server.progress", ctx.interaction.locale).format(percent=done))
        await asyncio.sleep(5)
        await msg.edit_original_response(content=localise("cog.fun.answers.crash_server.error", ctx.interaction.locale))

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.fun.commands.translate.name"),
        description_localizations=localise("cog.fun.commands.translate.desc"))
    async def translate(self, ctx: discord.ApplicationContext, mode: discord.Option(str,
            name_localizations=localise("cog.fun.commands.translate.options.mode.name"),
            description=localise("cog.fun.commands.translate.options.mode.desc", DEFAULT_LOCALE),
            description_localizations=localise("cog.fun.commands.translate.options.mode.desc"),
            choices=["to", "from"]
        ), language: discord.Option(str,
            name_localizations=localise("cog.fun.commands.translate.options.language.name"),
            description=localise("cog.fun.commands.translate.options.language.desc", DEFAULT_LOCALE),
            description_localizations=localise("cog.fun.commands.translate.options.language.desc"),
            choices=list(languages.languages.keys())
        ), text: discord.Option(str,
            name_localizations=localise("cog.fun.commands.translate.options.text.name"),
            description=localise("cog.fun.commands.translate.options.text.desc", DEFAULT_LOCALE),
            description_localizations=localise("cog.fun.commands.translate.options.text.desc")
        )):
        translated = languages.languages[language].translate(mode, text)
        await ctx.respond(
            localise("cog.fun.answers.translate.done", ctx.interaction.locale).format(
                text=text, language=language, translated=translated, way = localise(f"cog.fun.answers.translate.{mode}", ctx.interaction.locale)
                ), ephemeral=True)


def setup(bot):
    bot.add_cog(fun(bot))
