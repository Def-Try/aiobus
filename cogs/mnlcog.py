import discord
from discord.ext import commands

from mnlcore.engine_v4 import MnLEngine
from mnlcore.exceptions import BaseError
from mnlcore.libs import FakeIO

import json
with open("config.cfg", 'r') as f:
    CONFIG = json.loads(f.read())

class template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.engines = {}

    mnlcmds = discord.SlashCommandGroup("мнл", "Команды MnLCore")

    @mnlcmds.command(guild_ids=CONFIG["g_ids"], name="инит", desc="Инициализировать личный MnLEngine")
    async def init(self, ctx: discord.ApplicationContext):
        if ctx.author.id in self.engines.keys():
            await ctx.respond("Ваш МнЛ движок уже инициалищирован!")
            return
        self.engines[ctx.author.id] = MnLEngine()
        self.engines[ctx.author.id].fio = self.engines[ctx.author.id].load_library(FakeIO)
        await ctx.respond("МнЛ движок готов.")

    @mnlcmds.command(guild_ids=CONFIG["g_ids"], name="выполнить", desc="Запустить код в МнЛ Движке")
    async def run(self, ctx: discord.ApplicationContext, code: str):
        if not ctx.author.id in self.engines.keys():
            await ctx.respond("МнЛ движок не готов!")
            return
        try:
            self.engines[ctx.author.id].run(code)
        except BaseError as e:
            await ctx.respond(f"Ошибка во время выполнения: `{e}`\nВывод:\n```\n{self.engines[ctx.author.id].fio.read_output()}\n```")
            return
        await ctx.respond(f"Выполнение завершено!\nВывод:\n```\n{self.engines[ctx.author.id].fio.read_output()}\n```")


def setup(bot):
    bot.add_cog(template(bot))
