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
        if self.db.search(Query().channel == channel.id):
            await ctx.respond(localise("cog.starboard.answers.init.channel_already_init", ctx.interction.locale))
            return
        self.db.insert({"channel": channel.id, "guild": channel.guild.id, "limit": limit, "messages": {}})
        await ctx.respond(localise("cog.starboard.answers.init.ok", ctx.interaction.locale))

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.starboard.commands.destroy.name"),
        description_localizations=localise("cog.starboard.commands.destroy.desc"))
    async def destroy(self, ctx: discord.ApplicationContext, channel: discord.Option(discord.TextChannel,
            name_localizations=localise("cog.starboard.commands.destroy.options.channel.name"),
            description=localise("cog.starboard.commands.destroy.options.channel.desc", DEFAULT_LOCALE),
            description_localizations=localise("cog.starboard.commands.destroy.options.channel.desc"),
        )):
        starboard = self.db.search(Query().channel == channel.id)
        if not starboard:
            await ctx.respond(localise("cog.starboard.answers.destroy.not_found", ctx.interaction.locale))
            return
        self.db.remove(Query().channel == channel.id)
        await ctx.respond(localise("cog.starboard.answers.destroy.ok", ctx.interaction.locale))



    @commands.Cog.listener("on_raw_reaction_add")
    @commands.Cog.listener("on_raw_reaction_remove")
    async def starboard_react(self, payload):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        starboards = self.db.search(Query().guild == message.guild.id)
        if not starboards: return
        stars = list(filter(lambda rc: rc.emoji == self.emoji, message.reactions))
        if len(stars) == 0: star_amount = 0
        else: star_amount = stars[0].count
        for starboard in starboards:
            if star_amount < starboard["limit"] and str(message.id) not in starboard["messages"].keys():
                continue
            if star_amount < starboard["limit"]:
                await (await self.bot.get_channel(starboard["channel"]).fetch_message(starboard["messages"][str(message.id)])).delete()
                del starboard["messages"][str(message.id)]
                self.db.update(starboard, Query().guild == message.guild.id)
                continue
            embed = discord.Embed(title=f"{star_amount}{self.emoji}",description=message.content)
            embed.set_author(
                name=message.author.name if not hasattr(message.author, "nick") or not message.author.nick else message.author.nick,
                icon_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url
                )
            embeds = [embed] + message.embeds if not message.channel.nsfw else []
            files = [i.to_file() for i in message.attachments] if not message.channel.nsfw else []
            if str(message.id) in starboard["messages"].keys():
                starmessage = await self.bot.get_channel(starboard["channel"]).fetch_message(starboard["messages"][str(message.id)])
                await starmessage.edit(embeds=embeds, files=files)
            else:
                starboard["messages"][str(message.id)] = (await self.bot.get_channel(starboard["channel"]).send(embeds=embeds, files=files)).id
            self.db.update(starboard, Query().guild == message.guild.id)

def setup(bot):
    bot.add_cog(starboard(bot))
