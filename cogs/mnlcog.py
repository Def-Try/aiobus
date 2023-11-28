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
with open("config.cfg", 'r') as f:
    CONFIG = json.loads(f.read())

class template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.engines = {}

    mnlcmds = discord.SlashCommandGroup("мнл", "Команды MnLCore")

    @mnlcmds.command(guild_ids=CONFIG["g_ids"], name="инит", desc="Инициализировать MnLEngine")
    async def init(self, ctx: discord.ApplicationContext):
        if ctx.author.id in self.engines.keys():
            await ctx.respond("⚠️Ваш МнЛ движок уже инициализирован!")
            return
        self.engines[ctx.author.id] = MnLEngine()
        self.engines[ctx.author.id].persisting_globals = False
        self.engines[ctx.author.id].fio = self.engines[ctx.author.id].load_library(FakeIO)
        await ctx.respond("✅МнЛ движок готов.")

    @mnlcmds.command(guild_ids=CONFIG["g_ids"], name="конфиг", desc="Настроить MnLEngine")
    async def configure(self, ctx: discord.ApplicationContext, cfgname: discord.Option(str, choices=['persistent']), cfgval: str):
        if not ctx.author.id in self.engines.keys():
            await ctx.respond("⚠️МнЛ движок не готов!")
            return
        engine = self.engines[ctx.author.id]
        if cfgname == "persistent":
            engine.persisting_globals = True if cfgval in ["T", "True", "true", "t", "1", "yes", "y"] else False
            if engine.persisting_globals:
                await ctx.respond("✅Теперь переменные кода будут сохраняться между запусками.")
            else:
                await ctx.respond("✅Теперь переменные кода не будут сохраняться между запусками.")
            return

    @mnlcmds.command(guild_ids=CONFIG["g_ids"], name="выполнить", desc="Запустить код в MnLEngine")
    async def run(self, ctx: discord.ApplicationContext, code: str):
        if not ctx.author.id in self.engines.keys():
            await ctx.respond("⚠️МнЛ движок не готов!")
            return
        engine = self.engines[ctx.author.id]
        try:
            engine.run(code)
        except BaseError as e:
            output = engine.fio.read_output()
            await ctx.respond(f"⚠️Ошибка во время выполнения: `{e}`" + (f"\nВывод:\n```\n{output}\n```" if output else ""))
            return
        except Exception as e:
            await ctx.respond(f"❌Критическая ошибка во время выполнения: `{e}`")
        output = engine.fio.read_output()
        await ctx.respond(f"✅Выполнение завершено!" + (f"\nВывод:\n```\n{output}\n```" if output else ""))


def setup(bot):
    bot.add_cog(template(bot))
