import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from config import CONFIG
from localisation import localise, DEFAULT_LOCALE


class Starboard(commands.Cog):
    author = "googer_"
    emoji = "⭐"

    def __init__(self, bot):
        self.bot = bot
        self.db = TinyDB("databases/starboard.db")

    cmds = discord.SlashCommandGroup(
        "starboard",
        "",
        name_localizations=localise("cog.starboard.command_group.name"),
        description_localizations=localise("cog.starboard.command_group.desc"),
    )

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.starboard.commands.init.name"),
        description_localizations=localise("cog.starboard.commands.init.desc"),
    )
    @discord.default_permissions(administrator=True)
    async def init(
        self,
        ctx: discord.ApplicationContext,
        channel: discord.Option(
            discord.TextChannel,
            name_localizations=localise(
                "cog.starboard.commands.init.options.channel.name"
            ),
            description=localise(
                "cog.starboard.commands.init.options.channel.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.starboard.commands.init.options.channel.desc"
            ),
        ),
        limit: discord.Option(
            int,
            name_localizations=localise(
                "cog.starboard.commands.init.options.limit.name"
            ),
            description=localise(
                "cog.starboard.commands.init.options.limit.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.starboard.commands.init.options.limit.desc"
            ),
            min_value=1,
        ),
    ):
        if channel.guild != ctx.message.guild:
            await ctx.respond(
                localise(
                    "cog.starboard.answers.init.wrong_guild", ctx.interaction.locale
                )
            )
            return
        if self.db.search(Query().channel == channel.id):
            await ctx.respond(
                localise(
                    "cog.starboard.answers.init.channel_already_init",
                    ctx.interction.locale,
                )
            )
            return
        self.db.insert(
            {
                "channel": channel.id,
                "guild": channel.guild.id,
                "limit": limit,
                "messages": {},
            }
        )
        await ctx.respond(
            localise("cog.starboard.answers.init.ok", ctx.interaction.locale)
        )

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.starboard.commands.destroy.name"),
        description_localizations=localise("cog.starboard.commands.destroy.desc"),
    )
    @discord.default_permissions(administrator=True)
    async def destroy(
        self,
        ctx: discord.ApplicationContext,
        channel: discord.Option(
            discord.TextChannel,
            name_localizations=localise(
                "cog.starboard.commands.destroy.options.channel.name"
            ),
            description=localise(
                "cog.starboard.commands.destroy.options.channel.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.starboard.commands.destroy.options.channel.desc"
            ),
        ),
    ):
        if channel.guild != ctx.message.guild:
            await ctx.respond(
                localise(
                    "cog.starboard.answers.destroy.wrong_guild", ctx.interaction.locale
                )
            )
            return
        server_starboard = self.db.search(Query().channel == channel.id)
        if not server_starboard:
            await ctx.respond(
                localise(
                    "cog.starboard.answers.destroy.not_found", ctx.interaction.locale
                )
            )
            return
        self.db.remove(Query().channel == channel.id)
        await ctx.respond(
            localise("cog.starboard.answers.destroy.ok", ctx.interaction.locale)
        )

    @commands.Cog.listener("on_raw_reaction_add")
    @commands.Cog.listener("on_raw_reaction_remove")
    async def starboard_react(self, payload):
        message = await self.bot.get_channel(payload.channel_id).fetch_message(
            payload.message_id
        )
        starboards = self.db.search(Query().guild == message.guild.id)
        if not starboards:
            return
        stars = list(filter(lambda rc: rc.emoji == self.emoji, message.reactions))
        if len(stars) == 0:
            star_amount = 0
        else:
            star_amount = stars[0].count
        for server_starboard in starboards:
            if (
                star_amount < server_starboard["limit"]
                and str(message.id) not in server_starboard["messages"].keys()
            ):
                continue
            if star_amount < server_starboard["limit"]:
                await (
                    await self.bot.get_channel(
                        server_starboard["channel"]
                    ).fetch_message(server_starboard["messages"][str(message.id)])
                ).delete()
                del server_starboard["messages"][str(message.id)]
                self.db.update(server_starboard, Query().guild == message.guild.id)
                continue
            content = f"{star_amount}{self.emoji}"
            embed = discord.Embed(
                title="Jump!", description=message.content, url=message.jump_url
            )
            embed.set_author(
                name=(
                    message.author.name
                    if not hasattr(message.author, "nick") or not message.author.nick
                    else message.author.nick
                ),
                icon_url=(
                    message.author.avatar.url
                    if message.author.avatar
                    else message.author.default_avatar.url
                ),
            )
            embeds = [embed] + message.embeds if not message.channel.nsfw else []
            files = (
                [await i.to_file() for i in message.attachments]
                if not message.channel.nsfw
                else []
            )
            if str(message.id) in server_starboard["messages"].keys():
                starmessage = await self.bot.get_channel(
                    server_starboard["channel"]
                ).fetch_message(server_starboard["messages"][str(message.id)])
                await starmessage.edit(content=content, embeds=embeds, files=files)
            else:
                server_starboard["messages"][str(message.id)] = (
                    await self.bot.get_channel(server_starboard["channel"]).send(
                        content=content, embeds=embeds, files=files
                    )
                ).id
            self.db.update(server_starboard, Query().guild == message.guild.id)


def setup(bot):
    bot.add_cog(Starboard(bot))
