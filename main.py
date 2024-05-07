import json
import logging
import sys
import time
import traceback

import colorama
import discord
import termcolor
from discord.ext import commands

from config import CONFIG
from config import TOKENS

# pylint: disable=broad-exception-caught
try:
    colorama.just_fix_windows_console()
except Exception:
    pass
# pylint: enable=broad-exception-caught

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

try:
    from localisation import localise
except json.JSONDecodeError as uh_oh_json_error:
    logger.error(f"Localisation error: JSON could not be decoded: {uh_oh_json_error}")
    sys.exit(1)

discord_bot = commands.Bot(intents=discord.Intents.all())

discord_bot.logger = logger
discord_bot.ready = False


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


invoker = discord_bot.invoke_application_command


async def on_application_command(ctx: commands.Context):
    potentials = []
    for _, cog in discord_bot.cogs.items():
        for command in cog.walk_commands():
            try:
                if command.qualified_id != ctx.command.qualified_id:
                    continue
            except:
                continue
            potentials.append(command)

    def construct_name(data):
        command = data["name"]
        if len(data["options"]) == 1 and data["options"][0]["type"] == 1:
            command += " " + construct_name(data["options"][0])
        return command

    command_name = construct_name(ctx.interaction.data)
    command = None
    for potential in potentials:
        if potential.qualified_name != command_name:
            continue
        command = potential
        break
    ctx.res_command = command

    basic_cog = discord_bot.get_cog("basic")
    if not basic_cog:
        # basic cog isn't loaded, which is bad but we can handle that
        return await invoker(ctx)
    if not hasattr(ctx, "guild"):
        # we're probably running in DMs, so we'll ignore that case
        return await invoker(ctx)
    if (
        hasattr(ctx.res_command, "ignores_allowance")
        and ctx.res_command.ignores_allowance
    ):
        # command wants to ignore these limits so we dont try to stop it
        return await invoker(ctx)
    server_cfg = basic_cog.configs[str(ctx.guild.id)]["command_invoke"]
    channel = None
    if isinstance(ctx.channel.type, discord.Thread):
        channel = ctx.channel.parent
    else:
        channel = ctx.channel
    if (
        server_cfg["mode"] == "blacklist"
    ):  # server command invokation is in blacklist mode
        if channel.id in server_cfg["channels"]:
            await ctx.respond(
                localise("generic.error.blacklisted", ctx.interaction.locale),
                ephemeral=True,
            )
            return  # channel is blacklisted...
        return await invoker(ctx)
    # server command invokation is in whitelist mode
    if channel.id not in server_cfg["channels"]:
        await ctx.respond(
            localise("generic.error.notwhitelisted", ctx.interaction.locale),
            ephemeral=True,
        )
        return  # channel is not whitelisted...
    return await invoker(ctx)


discord_bot.invoke_application_command = on_application_command


@discord_bot.event
async def before_identify_hook(shard_id, *, initial=False):
    pass


@discord_bot.event
async def on_application_command_error(
    ctx: commands.Context, error: commands.CommandError
):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond(
            localise(
                "generic.error.missing_permissions", ctx.interaction.locale
            ).format(permissions=", ".join(error.missing_permissions))
        )
        return
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(
            localise("generic.error.cooldown", ctx.interaction.locale).format(
                retry_after=round(error.retry_after)
            )
        )
        return
    if isinstance(error, commands.NSFWChannelRequired):
        await ctx.respond(
            localise("generic.error.nsfw_required", ctx.interaction.locale)
        )
        return
    raise error


@discord_bot.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    if not reaction.message.author.id == discord_bot.user.id:
        return
    if not reaction.message.interaction:
        return
    if str(reaction) != "❌":
        return
    if not reaction.message.interaction.user == user:
        return

    await reaction.message.delete()


if __name__ == "__main__":
    discord_bot.reload_cogs = reload_cogs

    @discord_bot.event
    async def on_ready():
        discord_bot.ready = True
        discord_bot.logger.info(f"We have logged in as {discord_bot.user}")

    discord_bot.loaded_cogs = []
    _, _, _ = discord_bot.reload_cogs(discord_bot)

    discord_bot.run(TOKENS["discord"])
