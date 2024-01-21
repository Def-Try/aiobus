import discord
from discord.ext import commands
import logging
import asyncio
import colorama
import termcolor
import json
import time
import traceback

from config import CONFIG, TOKEN

colorama.just_fix_windows_console()

FORMAT = (
    termcolor.colored("[%(asctime)s]", "white", "on_cyan")
    + " "
    + termcolor.colored("[%(levelname)s]", "white", "on_blue")
    + " "
    + "%(message)s"
)
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("root")
logger.setLevel(logging.INFO)

# pylint: disable=unused-import
# This is used to check localisation, but is not used in main.
try:
    import localisation
except json.JSONDecodeError as e:
    logger.error(f"Localisation error: JSON could not be decoded: {e}")
    exit(1)
# pylint: enable=unused-import

bot = commands.Bot(intents=discord.Intents.all())

bot.logger = logger


def reload_cogs(bot):
    bot.logger.info(f"Reloading cogs...")

    timings = {"load": {}, "unload": {}}

    unload_fails = []
    load_fails = []
    for name in bot._cogs:
        start = time.perf_counter()
        try:
            bot.unload_extension(name)
            timings["unload"][name] = round((time.perf_counter() - start) * 1000, 2)
            bot.logger.info(f"Unloaded cog {name}")
        except Exception as e:
            timings["unload"][name] = round((time.perf_counter() - start) * 1000, 2)
            bot.logger.error(f"Fatal error while unloading cog {name}: {e}")
            traceback.print_exc()
            unload_fails.append(name)

    bot._cogs = []

    for cog in CONFIG["cogs"]:
        start = time.perf_counter()
        if cog in unload_fails:
            timings["load"][cog] = round((time.perf_counter() - start) * 1000, 2)
            bot.logger.info(
                f"Skipping loading of cog {cog} due to previous unload error."
            )
            continue
        try:
            bot.load_extension(cog)
            timings["load"][cog] = round((time.perf_counter() - start) * 1000, 2)
            bot.logger.info(f"Loaded cog {cog}")
            bot._cogs.append(cog)
        except Exception as e:
            timings["load"][cog] = round((time.perf_counter() - start) * 1000, 2)
            bot.logger.error(f"Fatal error while loading cog {cog}: {e}")
            traceback.print_exc()
            load_fails.append(cog)

    return unload_fails + load_fails, bot._cogs, timings


if __name__ == "__main__":
    bot.reload_cogs = reload_cogs

    @bot.event
    async def on_ready():
        bot.logger.info(f"We have logged in as {bot.user}")

    #    await reload_cogs()

    bot._cogs = []
    _, _, _ = bot.reload_cogs(bot)

    bot.run(TOKEN)
