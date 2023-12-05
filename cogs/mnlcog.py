import discord
from discord.ext import commands

try:
    from mnlcore.engine_v4 import MnLEngine
    from mnlcore.exceptions import BaseError
    from mnlcore.libs import FakeIO
except ImportError:
    from MnLEsolang.mnlcore.engine_v4 import MnLEngine
    from MnLEsolang.mnlcore.exceptions import BaseError
    from MnLEsolang.mnlcore.libs import FakeIO
import json
from localisation import LOCALISATIONS
with open("config.cfg", 'r') as f:
    CONFIG = json.loads(f.read())

class template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.engines = {}

    mnlcmds = discord.SlashCommandGroup("mnl", "",
        name_localizations=LOCALISATIONS["cog"]["mnlcog"]["command_group"]["name"],
        description_localisations=LOCALISATIONS["cog"]["mnlcog"]["command_group"]["desc"])

    @mnlcmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["mnlcog"]["commands"]["init"]["name"],
        description_localisations=LOCALISATIONS["cog"]["mnlcog"]["commands"]["init"]["desc"])
    async def init(self, ctx: discord.ApplicationContext):
        locale = ctx.interaction.locale
        if ctx.author.id in self.engines.keys():
            await ctx.respond(LOCALISATIONS["cog"]["mnlcog"]["answers"]["init"]["already_initialised"].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}"))
            return
        self.engines[ctx.author.id] = MnLEngine()
        self.engines[ctx.author.id].persisting_globals = False
        self.engines[ctx.author.id].fio = self.engines[ctx.author.id].load_library(FakeIO)
        await ctx.respond(LOCALISATIONS["cog"]["mnlcog"]["answers"]["init"]["ready"].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}"))

    @mnlcmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["mnlcog"]["commands"]["config"]["name"],
        description_localisations=LOCALISATIONS["cog"]["mnlcog"]["commands"]["config"]["desc"])
    async def configure(self, ctx: discord.ApplicationContext, cfgname: discord.Option(str, choices=['persistent']), cfgval: str):
        if not ctx.author.id in self.engines.keys():
            await ctx.respond(LOCALISATIONS["cog"]["mnlcog"]["answers"]["not_ready"].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}"))
            return
        engine = self.engines[ctx.author.id]
        if cfgname == "persistent":
            engine.persisting_globals = True if cfgval in ["T", "True", "true", "t", "1", "yes", "y"] else False
            if engine.persisting_globals:
                await ctx.respond(LOCALISATIONS["cog"]["mnlcog"]["answers"]["config"]["persisting_globals"]["true"].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}"))
            else:
                await ctx.respond(LOCALISATIONS["cog"]["mnlcog"]["answers"]["config"]["persisting_globals"]["false"].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}"))
            return

    @mnlcmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["mnlcog"]["commands"]["run"]["name"],
        description_localisations=LOCALISATIONS["cog"]["mnlcog"]["commands"]["run"]["desc"])
    async def run(self, ctx: discord.ApplicationContext, code: str):
        if not ctx.author.id in self.engines.keys():
            await ctx.respond(LOCALISATIONS["cog"]["mnlcog"]["answers"]["not_ready"].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}"))
            return
        await ctx.response.defer()
        engine = self.engines[ctx.author.id]
        timeout = 10
        try:
            await engine.run_nonblocking(code, timeout)
        except BaseError as e:
            output = engine.fio.read_output()
            await ctx.followup.send(LOCALISATIONS["cog"]["mnlcog"]["answers"]["run"]["mnl_error"][("with" if output else "no")+"_output"].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}").format(error=str(e), output=output))
            return
        except TimeoutError as e:
            output = engine.fio.read_output()
            await ctx.followup.send(LOCALISATIONS["cog"]["mnlcog"]["answers"]["run"]["timed_out"][("with" if output else "no")+"_output"].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}").format(timeout=str(timeout), output=output))
            return
        except Exception as e:
            await ctx.followup.send(LOCALISATIONS["cog"]["mnlcog"]["answers"]["run"]["fatal_error"][("with" if output else "no")+"_output"].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}").format(error=str(e), output=output))
            return
        output = engine.fio.read_output()
        await ctx.followup.send(LOCALISATIONS["cog"]["mnlcog"]["answers"]["run"]["ok"][("with" if output else "no")+"_output"].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}").format(output=output))


def setup(bot):
    bot.add_cog(template(bot))
