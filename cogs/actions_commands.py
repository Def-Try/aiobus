import discord
from discord.ext import commands
from nekosbest import Client

from config import CONFIG
from localisation import DEFAULT_LOCALE
from localisation import localise

nekosbest_client = Client()

# users banned entirely from this cog commands, basically
# turely_159 / UID 781110424783290388: spams them a bunch. does not know when to stop.
actions_bans = [
    781110424783290388,  # @turely_159
]


class ActionsCommands(commands.Cog, name="actions_commands"):
    author = "googer_"

    def __init__(self, bot):
        self.bot = bot

    acts_1 = discord.SlashCommandGroup(
        "actions_1",
        name_localizations=localise("cog.actions_commands.command_group.name"),
        description_localizations=localise("cog.actions_commands.command_group.desc"),
    )
    acts_2 = discord.SlashCommandGroup(
        "actions_2",
        name_localizations=localise("cog.actions_commands.command_group.name"),
        description_localizations=localise("cog.actions_commands.command_group.desc"),
    )

    async def act(self, action: str, ctx: discord.ApplicationContext):
        """action command. requires action itself and discord context."""
        if ctx.author.id in actions_bans:
            await ctx.respond(
                localise("generic.banned_from_command", ctx.interaction.locale),
                ephemeral=True,
            )
            return
        result = await nekosbest_client.get_image(action, 1)
        locale = ctx.interaction.locale
        localis_act = localise(
            f"cog.actions_commands.answers.action.{action}.self", ctx.interaction.locale
        )
        embed = discord.Embed(
            title=localise("cog.actions_commands.answers.action.name", locale),
            description=localis_act.format(member=ctx.author.mention),
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    async def act_req_other(
        self, action: str, ctx: discord.ApplicationContext, other: discord.Member
    ):
        """action command. requires action itself, other member, and discord context."""
        if ctx.author.id in actions_bans:
            await ctx.respond(
                localise("generic.banned_from_command", ctx.interaction.locale),
                ephemeral=True,
            )
            return
        result = await nekosbest_client.get_image(action, 1)
        locale = ctx.interaction.locale
        localis_act_self = localise(
            f"cog.actions_commands.answers.action.{action}.self", ctx.interaction.locale
        )
        localis_act_bot = localise(
            f"cog.actions_commands.answers.action.{action}.bot", ctx.interaction.locale
        )
        localis_act_other = localise(
            f"cog.actions_commands.answers.action.{action}.other",
            ctx.interaction.locale,
        )
        embed = discord.Embed(
            title=localise("cog.actions_commands.answers.action.name", locale),
            description=(
                localis_act_self.format(member=ctx.author.mention)
                if other == ctx.author
                else (
                    localis_act_bot.format(
                        member=ctx.author.mention, bot=self.bot.user.mention
                    )
                    if other == self.bot.user
                    else localis_act_other.format(
                        member=ctx.author.mention, other=other.mention
                    )
                )
            ),
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    async def act_with_other(
        self,
        action: str,
        ctx: discord.ApplicationContext,
        other: discord.Member = None,
    ):
        """action command. requires action itself, optionally other member, and discord context."""
        if ctx.author.id in actions_bans:
            await ctx.respond(
                localise("generic.banned_from_command", ctx.interaction.locale),
                ephemeral=True,
            )
            return
        result = await nekosbest_client.get_image(action, 1)
        locale = ctx.interaction.locale
        localis_act_self = localise(
            f"cog.actions_commands.answers.action.{action}.self", ctx.interaction.locale
        )
        localis_act_bot = localise(
            f"cog.actions_commands.answers.action.{action}.bot", ctx.interaction.locale
        )
        localis_act_other = localise(
            f"cog.actions_commands.answers.action.{action}.other",
            ctx.interaction.locale,
        )
        localis_act_none = localise(
            f"cog.actions_commands.answers.action.{action}.none", ctx.interaction.locale
        )
        embed = discord.Embed(
            title=localise("cog.actions_commands.answers.action.name", locale),
            description=(
                localis_act_self.format(member=ctx.author.mention)
                if other == ctx.author
                else (
                    localis_act_bot.format(
                        member=ctx.author.mention, bot=self.bot.user.mention
                    )
                    if other == self.bot.user
                    else (
                        localis_act_other.format(
                            member=ctx.author.mention, other=other.mention
                        )
                        if other
                        else localis_act_none.format(member=ctx.author.mention)
                    )
                )
            ),
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    # регион ПЕРВАЯ ГРУППА
    #  регион ОБЫЧНЫЕ ДЕЙСТВИЯ

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.pat"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def pat(
        self,
        ctx: discord.ApplicationContext,
        other: discord.Option(
            discord.Member,
            name_localizations=localise(
                "cog.actions_commands.commands.action.options.other.name"
            ),
            description=localise(
                "cog.actions_commands.commands.action.options.other.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.actions_commands.commands.action.options.other.desc"
            ),
        ),
    ):
        await self.act_req_other("pat", ctx, other)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.hug"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def hug(
        self,
        ctx: discord.ApplicationContext,
        other: discord.Option(
            discord.Member,
            name_localizations=localise(
                "cog.actions_commands.commands.action.options.other.name"
            ),
            description=localise(
                "cog.actions_commands.commands.action.options.other.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.actions_commands.commands.action.options.other.desc"
            ),
        ),
    ):
        await self.act_req_other("hug", ctx, other)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.cuddle"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def cuddle(
        self,
        ctx: discord.ApplicationContext,
        other: discord.Option(
            discord.Member,
            name_localizations=localise(
                "cog.actions_commands.commands.action.options.other.name"
            ),
            description=localise(
                "cog.actions_commands.commands.action.options.other.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.actions_commands.commands.action.options.other.desc"
            ),
        ),
    ):
        await self.act_req_other("cuddle", ctx, other)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.handshake"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def handshake(
        self,
        ctx: discord.ApplicationContext,
        other: discord.Option(
            discord.Member,
            name_localizations=localise(
                "cog.actions_commands.commands.action.options.other.name"
            ),
            description=localise(
                "cog.actions_commands.commands.action.options.other.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.actions_commands.commands.action.options.other.desc"
            ),
        ),
    ):
        await self.act_req_other("handshake", ctx, other)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.bite"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def bite(
        self,
        ctx: discord.ApplicationContext,
        other: discord.Option(
            discord.Member,
            name_localizations=localise(
                "cog.actions_commands.commands.action.options.other.name"
            ),
            description=localise(
                "cog.actions_commands.commands.action.options.other.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.actions_commands.commands.action.options.other.desc"
            ),
        ),
    ):
        await self.act_req_other("bite", ctx, other)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.highfive"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def highfive(
        self,
        ctx: discord.ApplicationContext,
        other: discord.Option(
            discord.Member,
            name_localizations=localise(
                "cog.actions_commands.commands.action.options.other.name"
            ),
            description=localise(
                "cog.actions_commands.commands.action.options.other.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.actions_commands.commands.action.options.other.desc"
            ),
        ),
    ):
        await self.act_req_other("highfive", ctx, other)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.kiss"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def kiss(
        self,
        ctx: discord.ApplicationContext,
        other: discord.Option(
            discord.Member,
            name_localizations=localise(
                "cog.actions_commands.commands.action.options.other.name"
            ),
            description=localise(
                "cog.actions_commands.commands.action.options.other.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.actions_commands.commands.action.options.other.desc"
            ),
        ),
    ):
        await self.act_req_other("kiss", ctx, other)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.poke"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def poke(
        self,
        ctx: discord.ApplicationContext,
        other: discord.Option(
            discord.Member,
            name_localizations=localise(
                "cog.actions_commands.commands.action.options.other.name"
            ),
            description=localise(
                "cog.actions_commands.commands.action.options.other.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.actions_commands.commands.action.options.other.desc"
            ),
        ),
    ):
        await self.act_req_other("poke", ctx, other)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.slap"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def slap(
        self,
        ctx: discord.ApplicationContext,
        other: discord.Option(
            discord.Member,
            name_localizations=localise(
                "cog.actions_commands.commands.action.options.other.name"
            ),
            description=localise(
                "cog.actions_commands.commands.action.options.other.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.actions_commands.commands.action.options.other.desc"
            ),
        ),
    ):
        await self.act_req_other("slap", ctx, other)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.handhold"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def handhold(
        self,
        ctx: discord.ApplicationContext,
        other: discord.Option(
            discord.Member,
            name_localizations=localise(
                "cog.actions_commands.commands.action.options.other.name"
            ),
            description=localise(
                "cog.actions_commands.commands.action.options.other.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.actions_commands.commands.action.options.other.desc"
            ),
        ),
    ):
        await self.act_req_other("handhold", ctx, other)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.kick"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def kick(
        self,
        ctx: discord.ApplicationContext,
        other: discord.Option(
            discord.Member,
            name_localizations=localise(
                "cog.actions_commands.commands.action.options.other.name"
            ),
            description=localise(
                "cog.actions_commands.commands.action.options.other.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.actions_commands.commands.action.options.other.desc"
            ),
        ),
    ):
        await self.act_req_other("kick", ctx, other)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.punch"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def punch(
        self,
        ctx: discord.ApplicationContext,
        other: discord.Option(
            discord.Member,
            name_localizations=localise(
                "cog.actions_commands.commands.action.options.other.name"
            ),
            description=localise(
                "cog.actions_commands.commands.action.options.other.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.actions_commands.commands.action.options.other.desc"
            ),
        ),
    ):
        await self.act_req_other("punch", ctx, other)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.tickle"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def tickle(
        self,
        ctx: discord.ApplicationContext,
        other: discord.Option(
            discord.Member,
            name_localizations=localise(
                "cog.actions_commands.commands.action.options.other.name"
            ),
            description=localise(
                "cog.actions_commands.commands.action.options.other.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.actions_commands.commands.action.options.other.desc"
            ),
        ),
    ):
        await self.act_req_other("tickle", ctx, other)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.feed"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def feed(
        self,
        ctx: discord.ApplicationContext,
        other: discord.Option(
            discord.Member,
            name_localizations=localise(
                "cog.actions_commands.commands.action.options.other.name"
            ),
            description=localise(
                "cog.actions_commands.commands.action.options.other.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.actions_commands.commands.action.options.other.desc"
            ),
        ),
    ):
        await self.act_req_other("feed", ctx, other)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.stare"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def stare(
        self,
        ctx: discord.ApplicationContext,
        other: discord.Option(
            discord.Member,
            name_localizations=localise(
                "cog.actions_commands.commands.action.options.other.name"
            ),
            description=localise(
                "cog.actions_commands.commands.action.options.other.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.actions_commands.commands.action.options.other.desc"
            ),
        ) = None,
    ):
        await self.act_with_other("stare", ctx, other)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.wave"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def wave(
        self,
        ctx: discord.ApplicationContext,
        other: discord.Option(
            discord.Member,
            name_localizations=localise(
                "cog.actions_commands.commands.action.options.other.name"
            ),
            description=localise(
                "cog.actions_commands.commands.action.options.other.desc",
                DEFAULT_LOCALE,
            ),
            description_localizations=localise(
                "cog.actions_commands.commands.action.options.other.desc"
            ),
        ) = None,
    ):
        await self.act_with_other("wave", ctx, other)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.cry"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def cry(self, ctx: discord.ApplicationContext):
        await self.act("cry", ctx)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.dance"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def dance(self, ctx: discord.ApplicationContext):
        await self.act("dance", ctx)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.blush"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def blush(self, ctx: discord.ApplicationContext):
        await self.act("blush", ctx)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.happy"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def happy(self, ctx: discord.ApplicationContext):
        await self.act("happy", ctx)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.laugh"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def laugh(self, ctx: discord.ApplicationContext):
        await self.act("laugh", ctx)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.shrug"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def shrug(self, ctx: discord.ApplicationContext):
        await self.act("shrug", ctx)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.sleep"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def sleep(self, ctx: discord.ApplicationContext):
        await self.act("sleep", ctx)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.smile"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def smile(self, ctx: discord.ApplicationContext):
        await self.act("smile", ctx)

    @acts_1.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.think"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def think(self, ctx: discord.ApplicationContext):
        await self.act("think", ctx)

    #  конец региона ОБЫЧНЫЕ ДЕЙСТВИЯ
    # конец региона ПЕРВАЯ ГРУППА

    # регион ВТОРАЯ ГРУППА
    #  регион ОБЫЧНЫЕ ДЕЙСТВИЯ

    @acts_2.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.actions_commands.commands.nod"),
        description_localizations=localise("cog.actions_commands.commands.action.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def nod(self, ctx: discord.ApplicationContext):
        await self.act("nod", ctx)

    #  конец региона ОБЫЧНЫЕ ДЕЙСТВИЯ
    # конец региона ВТОРАЯ ГРУППА


def setup(bot):
    bot.add_cog(ActionsCommands(bot))
