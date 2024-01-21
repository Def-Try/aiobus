import logging
import json
import time
import traceback
import sys
import discord
from discord.ext import commands
import colorama
import termcolor
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
except json.JSONDecodeError as uh_oh_json_error:
    logger.error(f"Localisation error: JSON could not be decoded: {uh_oh_json_error}")
    sys.exit(1)
# pylint: enable=unused-import

discord_bot = commands.Bot(intents=discord.Intents.all())

discord_bot.logger = logger


def reload_cogs(bot):
    bot.logger.info("Reloading cogs...")

    timings = {"load": {}, "unload": {}}

    # pylint: disable=broad-exception-caught

    unload_fails = []
    load_fails = []
    for name in bot.loaded_cogs:
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

    bot.loaded_cogs = []

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
            bot.loaded_cogs.append(cog)
        except Exception as e:
            timings["load"][cog] = round((time.perf_counter() - start) * 1000, 2)
            bot.logger.error(f"Fatal error while loading cog {cog}: {e}")
            traceback.print_exc()
            load_fails.append(cog)

    # pylint: enable=broad-exception-caught

    return unload_fails + load_fails, bot.loaded_cogs, timings


if __name__ == "__main__":
    discord_bot.reload_cogs = reload_cogs

    @discord_bot.event
    async def on_ready():
        discord_bot.logger.info(f"We have logged in as {discord_bot.user}")

    discord_bot.loaded_cogs = []
    _, _, _ = discord_bot.reload_cogs(discord_bot)

    discord_bot.run(TOKEN)
