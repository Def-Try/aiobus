import discord
from discord.ext import commands, tasks
import datetime

import json
from config import CONFIG

OFFTOPIC_PREFIXES = ["//", "(("]

class rp_utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.away_from_keyboard_checks.start()

    rpu = discord.SlashCommandGroup("рп_утилиты", "Утилиты для менеджмента РП процесса")

    @rpu.command(guild_ids=CONFIG["g_ids"], name="очистить_оффтоп")
    async def clean_offtopic(self, ctx: discord.ApplicationContext):
        await ctx.response.defer()
        messages = list()
        async for message in ctx.channel.history(limit=1000):
            if (any([message.content.startswith(offtopic_start) for offtopic_start in OFFTOPIC_PREFIXES])
                    and datetime.datetime.now(message.created_at.tzinfo) - message.created_at <= datetime.timedelta(days=14) and not message.pinned):
                messages.append(message)
        await ctx.followup.send(f"Будет удалено {len(messages)} сообщен{'ие' if len(messages) == 1 or len(messages) % 10 == 1 else 'ия' if len(messages) % 10 in (2, 3, 4) else 'ий' if len(messages) % 10 in (5, 6, 7, 8, 9, 0) else 'хз'}.", delete_after=10)
        for i in range(0, len(messages), 100):
            await ctx.channel.delete_messages(messages[i:i+100], reason=f"Удаление оффтоп сообщений в РП канале (префикс сообщения один из {OFFTOPIC_PREFIXES})")

    @tasks.loop(seconds=300)
    async def away_from_keyboard_checks():
        pass

def setup(bot):
    bot.add_cog(rp_utils(bot))
