import discord
from discord.ext import commands
from tinydb import Query

from config import CONFIG
from localisation import DEFAULT_LOCALE
from localisation import localise


class Configurator(commands.Cog, name="configurator"):
    author = "googer_"

    def __init__(self, bot):
        self.bot = bot
        self.basic_cog = self.bot.get_cog("basic")
        if not self.basic_cog:
            raise Exception(
                "Configurator cog is not able to work without basic cog loaded!!!!"
            )
        self.ai_cog = self.bot.get_cog("ai")

    cmds = discord.SlashCommandGroup(
        "configurator",
        "",
        name_localizations=localise("cog.configurator.command_group.name"),
        description_localizations=localise("cog.configurator.command_group.desc"),
    )
    cmdinvkcfg = cmds.create_subgroup(
        "command_execution",
        "",
        name_localizations=localise(
            "cog.configurator.command_group.sub.command_execution.name"
        ),
        description_localizations=localise(
            "cog.configurator.command_group.sub.command_execution.desc"
        ),
    )
    cmdgraicfg = cmds.create_subgroup(
        "googerai",
        "",
        name_localizations=localise("cog.configurator.command_group.sub.googerai.name"),
        description_localizations=localise(
            "cog.configurator.command_group.sub.googerai.desc"
        ),
    )

    @cmdinvkcfg.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise(
            "cog.configurator.commands.command_execution.set_mode.name"
        ),
        description_localizations=localise(
            "cog.configurator.commands.command_execution.set_mode.desc"
        ),
    )
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def set_mode(
        self,
        ctx: discord.ApplicationContext,
        mode: discord.Option(
            str,
            name_localizations=localise(
                "cog.configurator.commands.command_execution.set_mode.options.mode.name"
            ),
            description=localise(
                "cog.configurator.commands.command_execution.set_mode.options.mode.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.configurator.commands.command_execution.set_mode.options.mode.desc"
            ),
            choices=["whitelist", "blacklist"],
        ),
    ):
        if (
            mode == "whitelist"
            and len(
                self.basic_cog.configs[str(ctx.guild.id)]["command_invoke"]["channels"]
            )
            == 0
        ):
            await ctx.respond(
                localise(
                    "cog.configurator.answers.command_execution.you_dont_want_to_do_this",
                    ctx.interaction.locale,
                )
            )
            return
        self.basic_cog.configs[str(ctx.guild.id)]["command_invoke"]["mode"] = mode
        await self.basic_cog.update_config(ctx.guild)
        await ctx.respond(
            localise(
                "cog.configurator.answers.command_execution.mode_set",
                ctx.interaction.locale,
            )
        )

    @cmdinvkcfg.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise(
            "cog.configurator.commands.command_execution.add_channel.name"
        ),
        description_localizations=localise(
            "cog.configurator.commands.command_execution.add_channel.desc"
        ),
    )
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def add_channel(
        self,
        ctx: discord.ApplicationContext,
        channel: discord.Option(
            discord.TextChannel,
            name_localizations=localise(
                "cog.configurator.commands.command_execution.add_channel.options.channel.name"
            ),
            description=localise(
                "cog.configurator.commands.command_execution.add_channel.options.channel.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.configurator.commands.command_execution.add_channel.options.channel.desc"
            ),
        ),
    ):
        text_channels_amount = len(
            [c for c in ctx.guild.channels if isinstance(c, discord.TextChannel)]
        )
        mode = self.basic_cog.configs[str(ctx.guild.id)]["command_invoke"]["mode"]
        if (
            mode == "blacklist"
            and len(
                self.basic_cog.configs[str(ctx.guild.id)]["command_invoke"]["channels"]
            )
            == text_channels_amount - 1
        ) or (
            mode == "whitelist"
            and len(
                self.basic_cog.configs[str(ctx.guild.id)]["command_invoke"]["channels"]
            )
            < 1
        ):
            await ctx.respond(
                localise(
                    "cog.configurator.answers.command_execution.you_dont_want_to_do_this",
                    ctx.interaction.locale,
                )
            )
            return
        self.basic_cog.configs[str(ctx.guild.id)]["command_invoke"]["channels"].append(
            channel.id
        )
        await self.basic_cog.update_config(ctx.guild)
        await ctx.respond(
            localise(
                "cog.configurator.answers.command_execution.channel_added",
                ctx.interaction.locale,
            )
        )

    @cmdinvkcfg.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise(
            "cog.configurator.commands.command_execution.remove_channel.name"
        ),
        description_localizations=localise(
            "cog.configurator.commands.command_execution.remove_channel.desc"
        ),
    )
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def remove_channel(
        self,
        ctx: discord.ApplicationContext,
        channel: discord.Option(
            discord.TextChannel,
            name_localizations=localise(
                "cog.configurator.commands.command_execution.remove_channel.options.channel.name"
            ),
            description=localise(
                "cog.configurator.commands.command_execution.remove_channel.options.channel.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.configurator.commands.command_execution.remove_channel.options.channel.desc"
            ),
        ),
    ):
        text_channels_amount = len(
            [c for c in ctx.guild.channels if isinstance(c, discord.TextChannel)]
        )
        mode = self.basic_cog.configs[str(ctx.guild.id)]["command_invoke"]["mode"]
        if (
            mode == "whitelist"
            and len(
                self.basic_cog.configs[str(ctx.guild.id)]["command_invoke"]["channels"]
            )
            < 2
        ):
            await ctx.respond(
                localise(
                    "cog.configurator.answers.command_execution.you_dont_want_to_do_this",
                    ctx.interaction.locale,
                )
            )
            return
        if (
            channel.id
            not in self.basic_cog.configs[str(ctx.guild.id)]["command_invoke"][
                "channels"
            ]
        ):
            await ctx.respond(
                localise(
                    "cog.configurator.answers.command_execution.channel_not_in_list",
                    ctx.interaction.locale,
                )
            )
            return
        self.basic_cog.configs[str(ctx.guild.id)]["command_invoke"]["channels"].pop(
            self.basic_cog.configs[str(ctx.guild.id)]["command_invoke"][
                "channels"
            ].index(channel.id)
        )
        await self.basic_cog.update_config(ctx.guild)
        await ctx.respond(
            localise(
                "cog.configurator.answers.command_execution.channel_removed",
                ctx.interaction.locale,
            )
        )

    @cmdinvkcfg.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise(
            "cog.configurator.commands.command_execution.show.name"
        ),
        description_localizations=localise(
            "cog.configurator.commands.command_execution.show.desc"
        ),
    )
    @commands.guild_only()
    async def show(self, ctx: discord.ApplicationContext):
        cfg = self.basic_cog.configs[str(ctx.guild.id)]["command_invoke"]
        await ctx.respond(
            localise(
                "cog.configurator.answers.command_execution.show",
                ctx.interaction.locale,
            ).format(
                mode=cfg["mode"],
                channels=", ".join([f"<#{ch}>" for ch in cfg["channels"]]),
            )
        )

    @cmdgraicfg.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.configurator.commands.googerai.set_mode.name"),
        description_localizations=localise(
            "cog.configurator.commands.googerai.set_mode.desc"
        ),
    )
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def set_mode(
        self,
        ctx: discord.ApplicationContext,
        mode: discord.Option(
            str,
            name_localizations=localise(
                "cog.configurator.commands.googerai.set_mode.options.mode.name"
            ),
            description=localise(
                "cog.configurator.commands.googerai.set_mode.options.mode.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.configurator.commands.googerai.set_mode.options.mode.desc"
            ),
            choices=["whitelist", "blacklist"],
        ),
    ):
        if not self.ai_cog:
            await ctx.respond(
                localise(
                    "cog.configurator.answers.googerai.unavaliable",
                    ctx.interaction.locale,
                )
            )
            return
        udata = self.ai_cog.get_udata(self.ai_cog.get_udata_id(ctx))
        self.ai_cog.udata[self.ai_cog.get_udata_id(ctx)] = udata

        udata["settings"]["allowmode"] = mode

        self.db.upsert(
            {
                "key": str(self.ai_cog.get_udata_id(ctx)),
                "data": self.ai_cog.udata[self.ai_cog.get_udata_id(ctx)],
            },
            Query().ai_cog.key == self.ai_cog.get_udata_id(ctx),
        )

        await ctx.respond(
            localise(
                "cog.configurator.answers.googerai.mode_set", ctx.interaction.locale
            )
        )

    @cmdgraicfg.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise(
            "cog.configurator.commands.googerai.add_channel.name"
        ),
        description_localizations=localise(
            "cog.configurator.commands.googerai.add_channel.desc"
        ),
    )
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def add_channel(
        self,
        ctx: discord.ApplicationContext,
        channel: discord.Option(
            discord.TextChannel,
            name_localizations=localise(
                "cog.configurator.commands.googerai.add_channel.options.channel.name"
            ),
            description=localise(
                "cog.configurator.commands.googerai.add_channel.options.channel.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.configurator.commands.googerai.add_channel.options.channel.desc"
            ),
        ),
    ):
        if not self.ai_cog:
            await ctx.respond(
                localise(
                    "cog.configurator.answers.googerai.unavaliable",
                    ctx.interaction.locale,
                )
            )
            return
        udata = self.ai_cog.get_udata(self.ai_cog.get_udata_id(ctx))
        self.ai_cog.udata[self.ai_cog.get_udata_id(ctx)] = udata

        udata["settings"]["list"].append(channel.id)

        self.db.upsert(
            {
                "key": str(self.ai_cog.get_udata_id(ctx)),
                "data": self.ai_cog.udata[self.ai_cog.get_udata_id(ctx)],
            },
            Query().ai_cog.key == self.ai_cog.get_udata_id(ctx),
        )

        await ctx.respond(
            localise(
                "cog.configurator.answers.googerai.channel_added",
                ctx.interaction.locale,
            )
        )

    @cmdgraicfg.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise(
            "cog.configurator.commands.googerai.remove_channel.name"
        ),
        description_localizations=localise(
            "cog.configurator.commands.googerai.remove_channel.desc"
        ),
    )
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def remove_channel(
        self,
        ctx: discord.ApplicationContext,
        channel: discord.Option(
            discord.TextChannel,
            name_localizations=localise(
                "cog.configurator.commands.googerai.remove_channel.options.channel.name"
            ),
            description=localise(
                "cog.configurator.commands.googerai.remove_channel.options.channel.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.configurator.commands.googerai.remove_channel.options.channel.desc"
            ),
        ),
    ):
        if not self.ai_cog:
            await ctx.respond(
                localise(
                    "cog.configurator.answers.googerai.unavaliable",
                    ctx.interaction.locale,
                )
            )
            return
        udata = self.ai_cog.get_udata(self.ai_cog.get_udata_id(ctx))
        self.ai_cog.udata[self.ai_cog.get_udata_id(ctx)] = udata

        udata["settings"]["list"].pop(udata["settings"]["list"].index(channel.id))

        self.db.upsert(
            {
                "key": str(self.ai_cog.get_udata_id(ctx)),
                "data": self.ai_cog.udata[self.ai_cog.get_udata_id(ctx)],
            },
            Query().ai_cog.key == self.ai_cog.get_udata_id(ctx),
        )

        await ctx.respond(
            localise(
                "cog.configurator.answers.googerai.channel_removed",
                ctx.interaction.locale,
            )
        )

    @cmdgraicfg.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.configurator.commands.googerai.show.name"),
        description_localizations=localise(
            "cog.configurator.commands.googerai.show.desc"
        ),
    )
    @commands.guild_only()
    async def show(self, ctx: discord.ApplicationContext):
        if not self.ai_cog:
            await ctx.respond(
                localise(
                    "cog.configurator.answers.googerai.unavaliable",
                    ctx.interaction.locale,
                )
            )
            return
        udata = self.ai_cog.get_udata(self.ai_cog.get_udata_id(ctx))
        self.ai_cog.udata[self.ai_cog.get_udata_id(ctx)] = udata
        await ctx.respond(
            localise(
                "cog.configurator.answers.googerai.show", ctx.interaction.locale
            ).format(
                mode=udata["settings"]["allowmode"],
                channels=", ".join([f"<#{ch}>" for ch in udata["settings"]["list"]]),
            )
        )


def setup(bot):
    bot.add_cog(Configurator(bot))
