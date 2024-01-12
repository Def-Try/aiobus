import discord
from discord.ext import commands
from localisation import localise
from config import CONFIG

import shutil

class debug(commands.Cog):
    author = "googer_'s blood and tears :sob:"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def init_on_ready(self):
        pass

    cmds = discord.SlashCommandGroup("debug", "",
        name_localizations=localise("cog.debug.command_group.name"),
        description_localizations=localise("cog.debug.command_group.desc"))

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.debug.commands.senddbs.name"),
        description_localizations=localise("cog.debug.commands.senddbs.desc"))
    @commands.is_owner()
    async def senddbs(self, ctx: discord.ApplicationContext):
        try:
            shutil.make_archive("temp/__TEMP_DEBUG_SENDDBS", 'zip', "databases")
        except:
            await ctx.respond(localise("cog.debug.answers.senddbs.cantzip", ctx.interaction.locale), ephemeral=True)
            return
        file = open("temp/__TEMP_DEBUG_SENDDBS.zip", 'rb')
        await ctx.respond(localise("cog.debug.answers.senddbs.ok", ctx.interaction.locale), ephemeral=True,
            file=discord.File(file, filename="databases.zip"))
        file.close()

def setup(bot):
    bot.add_cog(debug(bot))
