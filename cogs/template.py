import discord
from discord.ext import commands
from config import CONFIG
from localisation import localise
import json

class template(commands.Cog):
    author = "googer_"

    def __init__(self, bot):
        self.bot = bot

    cmds = discord.SlashCommandGroup("template", "",
        name_localizations=localise("cog.template.command_group.name"),
        description_localizations=localise("cog.template.command_group.desc"))

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.template.commands.cmd.name"),
        description_localizations=localise("cog.template.commands.cmd.desc"))
    async def cmd(self, ctx: discord.ApplicationContext):
        await ctx.respond(localise("cog.template.answers.cmd.text", ctx.interaction.locale))

def setup(bot):
    bot.add_cog(template(bot))
