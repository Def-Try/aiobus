import asyncio
import io

import aiohttp
import discord
from discord.ext import commands
from nekosbest import Client
from petpetgif import petpet as petpetgif

from config import CONFIG
from localisation import DEFAULT_LOCALE
from localisation import localise

nekosbest_client = Client()

categories = [
    "baka",
    "bite",
    "blush",
    "bored",
    "cry",
    "cuddle",
    "dance",
    "facepalm",
    "feed",
    "happy",
    "highfive",
    "hug",
    "kiss",
    "laugh",
    "neko",
    "pat",
    "poke",
    "pout",
    "shrug",
    "slap",
    "sleep",
    "smile",
    "smug",
    "stare",
    "think",
    "thumbsup",
    "tickle",
    "wave",
    "wink",
    "kitsune",
    "waifu",
    "handhold",
    "kick",
    "punch",
    "shoot",
    "husbando",
    "yeet",
    "nod",
    "nom",
    "nope",
    "handshake",
    "lurk",
    "peck",
    "yawn",
]


async def download_file(session, url):
    try:
        async with session.get(url) as remotefile:
            if remotefile.status == 200:
                data = await remotefile.read()
                return {"error": "", "data": data}
            return {"error": remotefile.status, "data": ""}
    except Exception as e:
        return {"error": e, "data": ""}


class GifRelated(commands.Cog, name="gif_related"):
    author = "googer_"

    def __init__(self, bot):
        self.bot = bot

    gif_cmds = discord.SlashCommandGroup(
        "gif",
        name_localizations=localise("cog.gif_related.command_group.name"),
        description_localizations=localise("cog.gif_related.command_group.desc"),
    )

    @gif_cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.gif_related.commands.findgif.name"),
        description_localizations=localise("cog.gif_related.commands.findgif.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def findgif(
        self,
        ctx: discord.ApplicationContext,
        category: discord.Option(
            str,
            name_localizations=localise(
                "cog.gif_related.commands.findgif.options.category.name"
            ),
            description=localise(
                "cog.gif_related.commands.findgif.options.category.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.gif_related.commands.findgif.options.category.desc"
            ),
        ),
    ):
        locale = ctx.interaction.locale
        if category not in categories:
            await ctx.respond(
                localise(
                    "cog.gif_related.answers.findgif.invalid_category", locale
                ).format(categories=", ".join(categories))
            )
            return
        result = await nekosbest_client.get_image(category, 1)
        embed = discord.Embed(
            title=localise("cog.gif_related.answers.findgif.title", locale),
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @gif_cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.gif_related.commands.shiggy.name"),
        description_localizations=localise("cog.gif_related.commands.shiggy.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def shiggy(self, ctx: discord.ApplicationContext):
        loop = asyncio.get_event_loop()
        con = aiohttp.TCPConnector(limit=10)
        async with aiohttp.ClientSession(loop=loop, connector=con) as session:
            status = await download_file(session, "https://shiggy.fun/api/v3/random")
            if status["error"]:
                await ctx.respond(status["error"])
                return
            with io.BytesIO(status["data"]) as fp:
                await ctx.respond(file=discord.File(fp, "shiggy.png"))

    @gif_cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.gif_related.commands.petpet.name"),
        description_localizations=localise("cog.gif_related.commands.petpet.desc"),
    )
    @commands.cooldown(10, 30, commands.BucketType.user)
    async def petpet(
        self,
        ctx: discord.ApplicationContext,
        member: discord.Option(
            discord.User,
            name_localizations=localise(
                "cog.gif_related.commands.petpet.options.member.name"
            ),
            description=localise(
                "cog.gif_related.commands.petpet.options.member.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.gif_related.commands.petpet.options.member.desc"
            ),
        ) = None,
        image: discord.Option(
            discord.Attachment,
            name_localizations=localise(
                "cog.gif_related.commands.petpet.options.image.name"
            ),
            description=localise(
                "cog.gif_related.commands.petpet.options.image.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.gif_related.commands.petpet.options.image.desc"
            ),
        ) = None,
    ):
        img = None
        name = None
        if member:
            img = await member.display_avatar.read()
            name = member.name
        if image:
            img = await image.read()
            name = "img"
        if not img:
            img = await ctx.author.display_avatar.read()
            name = ctx.author.name

        source = io.BytesIO(img)
        dest = io.BytesIO()
        try:
            petpetgif.make(source, dest)
        except Exception:
            await ctx.respond(
                localise("cog.gif_related.answers.petpet.fail", DEFAULT_LOCALE)
            )
            return
        dest.seek(0)
        await ctx.respond(file=discord.File(dest, filename=f"{name}-petpet.gif"))


def setup(bot):
    bot.add_cog(GifRelated(bot))
