import discord
from discord.ext import commands

import json
with open("config.cfg", 'r') as f:
    CONFIG = json.loads(f.read())

class basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=CONFIG["g_ids"])
    async def test_(self, ctx: discord.ApplicationContext):
        await ctx.respond("о это же я!")

    @commands.slash_command(guild_ids=CONFIG["g_ids"])
    async def reload_cogs(self, ctx: discord.ApplicationContext):
        msg = await ctx.respond("Перезагружаю...")
        failed_to_reload, ok_reload, timings = self.bot.reload_cogs(self.bot)
        embed = discord.Embed(
            title="Перезагрузка модулей",
            description=f"{len(failed_to_reload)} с ошибкой, {len(ok_reload)} успешно.",
            color=discord.Colour.blurple(),
        )
        for cog in failed_to_reload:
            embed.add_field(name=f"`[ОШИБКА]` {cog}", 
                            value=f"Время для выгрузки/загрузки: `{timings['unload'].get(cog, 'undefined')}ms`/`{timings['load'].get(cog, 'undefined')}ms`",
                            inline=False)
        for cog in ok_reload:
            embed.add_field(name=f"`[  ОК  ]` {cog}", 
                            value=f"Время для выгрузки/загрузки: `{timings['unload'].get(cog, 'undefined')}ms`/`{timings['load'].get(cog, 'undefined')}ms`",
                            inline=False)
        try:
            await self.bot.sync_commands(force=True)
            embed.add_field(name=f"Синхронизация",
                            value=f"Синхронизация команд успешна.",
                            inline=False)
        except Exception as e:
            self.bot.logger.warning(e)
            embed.add_field(name=f"Синхронизация",
                            value=f"Синхронизация команд не удалась.",
                            inline=False)
        await msg.edit_original_response(content="", embed=embed)

def setup(bot):
    bot.add_cog(basic(bot))
