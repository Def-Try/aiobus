import discord
from discord.ext import commands
from config import CONFIG
from localisation import localise, DEFAULT_LOCALE
from tinydb import TinyDB, Query
import json

class starboard(commands.Cog):
    author = "googer_"
    emoji = "⭐"

    def __init__(self, bot):
        self.bot = bot
        self.db = TinyDB('databases/starboard.db')

    cmds = discord.SlashCommandGroup("starboard", "",
        name_localizations=localise("cog.starboard.command_group.name"),
        description_localizations=localise("cog.starboard.command_group.desc"))

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.starboard.commands.init.name"),
        description_localizations=localise("cog.starboard.commands.init.desc"))
    async def init(self, ctx: discord.ApplicationContext, channel: discord.Option(discord.TextChannel,
            name_localizations=localise("cog.starboard.commands.init.options.channel.name"),
            description=localise("cog.starboard.commands.init.options.channel.desc", DEFAULT_LOCALE),
            description_localizations=localise("cog.starboard.commands.init.options.channel.desc"),
        ), limit: discord.Option(int,
            name_localizations=localise("cog.starboard.commands.init.options.limit.name"),
            description=localise("cog.starboard.commands.init.options.limit.desc", DEFAULT_LOCALE),
            description_localizations=localise("cog.starboard.commands.init.options.limit.desc"),
            min_value=1
        )):
        self.db.insert({"channel": channel.id, "limit": limit, "messages": []})
        await ctx.respond(localise("cog.starboard.answers.init.ok", ctx.interaction.locale))

    @commands.Cog.listener("on_raw_reaction_add")
    @commands.Cog.listener("on_raw_reaction_remove")
    async def starboard_reacadd(self, payload):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        starboards = self.db.search({"channel": message.channel.id})
        if not starboards: return
        stars = list(filter(lambda rc: rc.emoji == self.emoji, message.reactions))
        if len(stars) == 0: return
        star_amount = stars[0].count
        for starboard in starboards:
            if star_amount < starboard["limit"]: continue
            embed = discord.Embed(description=message.content)
            embed.set_author(name=message.author.name if not hasattr(message.author, "nick") or not message.author.nick else message.author.nick)
            if message.id in starboard["messages"].keys():
                starmessage = await self.bot.get_channel(starboard["channel"]).fetch_message(starboard["messages"][message.id])


def setup(bot):
    bot.add_cog(starboard(bot))
