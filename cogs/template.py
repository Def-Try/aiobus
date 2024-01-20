"""
template cog
aka How To Make Your Own Module
"""

import discord
from discord.ext import commands
from localisation import localise
from config import CONFIG


class template(commands.Cog):
    """
    first, Class Name.
    it should describe your cog in literally 1 to 2 words.
    also it usually is used in localisation strings, soo...

    author field in cog is used for Help commands coghelp.
    usually should be your nickname
    """

    author = "googer_"

    def __init__(self, bot):
        """
        cog init.
        this is where you put your initialisation shit, like...
          connecting to the DB
          preparing data / making aiohttp sessions
          etc...
        this is not an async function and it is tun before bot
        has connected to the Gateway
        """
        self.bot = bot

    @commands.Cog.listener("on_ready")
    async def init_on_ready(self):
        """
        cog init after bot is ready.
        is async and bot has connected to the Gateway
        """
        pass

    cmds = discord.SlashCommandGroup(
        "template",
        "",
        name_localizations=localise("cog.template.command_group.name"),
        description_localizations=localise("cog.template.command_group.desc"),
    )
    """
    cog's command group. PLEASE, use it instead of straight
    making command instead of putting it in a group

    also, about localise(localistring, locale=None)
    localistring is a json path, where dot is the divider.
    a.b.c.d path maps to json 
    {
        "a": {
            "b": {
                "c": {
                    "d": ...
                }
            }
        }
    }
    localisation files are located in BOTROOT/localisation/<locale>/strings
    ask me (googer_) for more info on that, idk how to explain it
    """

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.template.commands.cmd.name"),
        description_localizations=localise("cog.template.commands.cmd.desc"),
    )
    async def cmd(self, ctx: discord.ApplicationContext):
        await ctx.respond(
            localise("cog.template.answers.cmd.text", ctx.interaction.locale)
        )


def setup(bot):
    bot.add_cog(template(bot))
