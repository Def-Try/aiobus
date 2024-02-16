import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from localisation import localise, DEFAULT_LOCALE
from config import CONFIG


class AdminHelp(commands.Cog):
    author = "googer_"

    def __init__(self, bot):
        self.bot = bot
        self.db = TinyDB("databases/adminhelp.db")

    @commands.Cog.listener("on_ready")
    async def init_on_ready(self):
        self.bot.logger.info("AdminHelp cog loading!")
        self.interchat = self.bot.get_cog("interchat")
        if self.interchat is None:
            self.bot.logger.warning("Failed to load interchat integration.")
        else:
            self.bot.logger.info("Interchat integration loaded!")

    cmds = discord.SlashCommandGroup(
        "adminhelp",
        "",
        name_localizations=localise("cog.adminhelp.command_group.name"),
        description_localizations=localise("cog.adminhelp.command_group.desc"),
    )

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.adminhelp.commands.set_ahelp_channel.name"),
        description_localizations=localise(
            "cog.adminhelp.commands.set_ahelp_channel.desc"
        ),
    )
    @discord.default_permissions(administrator=True)
    @discord.has_guild_permissions(administrator=True)
    async def set_ahelp_channel(
        self,
        ctx: discord.ApplicationContext,
        channel: discord.Option(
            discord.TextChannel,
            name_localizations=localise(
                "cog.adminhelp.commands.set_ahelp_channel.options.channel.name"
            ),
            description=localise(
                "cog.adminhelp.commands.set_ahelp_channel.options.channel.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.adminhelp.commands.set_ahelp_channel.options.channel.desc"
            ),
        ),
    ):
        self.db.upsert(
            {"guild": ctx.guild.id, "ahelp_channel": channel.id},
            Query().guild == ctx.guild.id,
        )
        await ctx.respond(
            localise(
                "cog.adminhelp.answers.ahelp_channel_update", ctx.interaction.locale
            ).format(channel=channel.mention)
        )

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.adminhelp.commands.set_ahelp_role.name"),
        description_localizations=localise(
            "cog.adminhelp.commands.set_ahelp_role.desc"
        ),
    )
    @discord.default_permissions(administrator=True)
    @discord.has_guild_permissions(administrator=True)
    async def set_ahelp_role(
        self,
        ctx: discord.ApplicationContext,
        role: discord.Option(
            discord.Role,
            name_localizations=localise(
                "cog.adminhelp.commands.set_ahelp_role.options.role.name"
            ),
            description=localise(
                "cog.adminhelp.commands.set_ahelp_role.options.role.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.adminhelp.commands.set_ahelp_role.options.role.desc"
            ),
        ),
    ):
        self.db.upsert(
            {"guild": ctx.guild.id, "ahelp_role": role.id},
            Query().guild == ctx.guild.id,
        )
        await ctx.respond(
            localise(
                "cog.adminhelp.answers.ahelp_role_update", ctx.interaction.locale
            ).format(role=role.mention),
            allowed_mentions=discord.AllowedMentions.none(),
        )

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.adminhelp.commands.ahelp.name"),
        description_localizations=localise("cog.adminhelp.commands.ahelp.desc"),
    )
    async def ahelp(
        self,
        ctx: discord.ApplicationContext,
        message: discord.Option(
            str,
            name_localizations=localise(
                "cog.adminhelp.commands.ahelp.options.message.name"
            ),
            description=localise(
                "cog.adminhelp.commands.ahelp.options.message.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.adminhelp.commands.ahelp.options.message.desc"
            ),
        ),
    ):
        ahelp = self.db.search(Query().guild == ctx.guild.id)
        if len(ahelp) == 0:
            await ctx.respond(
                localise(
                    "cog.adminhelp.answers.ahelp.not_configured.overall",
                    ctx.interaction.locale,
                ),
                ephemeral=True,
            )
            return
        ahelp = ahelp[0]
        if ahelp.get("ahelp_channel") is None:
            await ctx.respond(
                localise(
                    "cog.adminhelp.answers.ahelp.not_configured.no_channel",
                    ctx.interaction.locale,
                ),
                ephemeral=True,
            )
            return
        if ahelp.get("ahelp_role") is None:
            await ctx.respond(
                localise(
                    "cog.adminhelp.answers.ahelp.not_configured.no_role",
                    ctx.interaction.locale,
                ),
                ephemeral=True,
            )
            return
        ahelp_ch = self.bot.get_channel(ahelp.get("ahelp_channel"))
        if not ahelp_ch:
            await ctx.respond(
                localise(
                    "cog.adminhelp.answers.ahelp.not_configured.no_channel",
                    ctx.interaction.locale,
                ),
                ephemeral=True,
            )
            return
        ahelp_role = ahelp_ch.guild.get_role(ahelp.get("ahelp_role"))
        if not ahelp_role:
            await ctx.respond(
                localise(
                    "cog.adminhelp.answers.ahelp.not_configured.no_role",
                    ctx.interaction.locale,
                ),
                ephemeral=True,
            )
            return
        embed = discord.Embed(
            title=localise("cog.adminhelp.answers.ahelp.embed.title", DEFAULT_LOCALE),
            description=localise(
                "cog.adminhelp.answers.ahelp.embed.description", DEFAULT_LOCALE
            ),
        )
        embed.set_author(
            name=ctx.author.name,
            icon_url=(
                ctx.author.avatar.url
                if ctx.author.avatar
                else ctx.author.default_avatar.url
            ),
        )
        embed.add_field(
            name=localise("cog.adminhelp.answers.ahelp.embed.message", DEFAULT_LOCALE),
            value=message,
            inline=False,
        )
        embed.add_field(
            name=localise("cog.adminhelp.answers.ahelp.embed.channel", DEFAULT_LOCALE),
            value=ctx.channel.mention,
            inline=False,
        )
        embed.add_field(
            name=localise(
                "cog.adminhelp.answers.ahelp.embed.requestor", DEFAULT_LOCALE
            ),
            value=ctx.author.mention,
            inline=False,
        )
        if self.interchat:
            embed.add_field(
                name=localise(
                    "cog.adminhelp.answers.ahelp.embed.interchat", DEFAULT_LOCALE
                ),
                value=self.interchat.get_address(await self.bot.create_dm(ctx.author)),
                inline=False,
            )
        await ahelp_ch.send(ahelp_role.mention, embed=embed)
        await ctx.respond(
            localise(
                "cog.adminhelp.answers.ahelp.message_sent", ctx.interaction.locale
            ),
            ephemeral=True,
        )


def setup(bot):
    bot.add_cog(AdminHelp(bot))
