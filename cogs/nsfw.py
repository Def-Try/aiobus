import io
import os
import random
import urllib

import aiohttp
import discord
from discord.ext import commands

from config import CONFIG
from config import TOKENS
from localisation import DEFAULT_LOCALE
from localisation import localise
from utilities import download_file


class Provider:
    @staticmethod
    def get_img_url(post):
        return post["url"]

    @staticmethod
    def get_posts(_):
        return {"url": "http://example.com"}


class R34:
    @staticmethod
    async def get_posts(tags):
        formatted_tags = ""
        for tag in tags:
            formatted_tags += tag
            formatted_tags += "+"
        if formatted_tags.endswith("+"):
            formatted_tags = formatted_tags[:-1]
        try:
            url = (
                "https://api.rule34.xxx/index.php?page=dapi&s=post&q=index"
                + f"&tags={formatted_tags}&limit=1000&pid=0&json=1"
            )
            headers = {
                "User-Agent": "Mozilla/5.0",
                "Host": "api.rule34.xxx",
                "Accept": "*/*",
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=5) as response:
                    request = await response.json()
        except TimeoutError:
            return {}
        if not request:
            return {}
        return request

    @staticmethod
    def get_img_url(post):
        return post.get("file_url")


class Danbooru:
    @staticmethod
    async def get_posts(tags):
        formatted_tags = ""
        for tag in tags:
            formatted_tags += tag
            formatted_tags += "+"
        if formatted_tags.endswith("+"):
            formatted_tags = formatted_tags[:-1]
        try:
            url = (
                f'https://{TOKENS["danbooru"]}@danbooru.donmai.us/posts.json?'
                + f"tags={formatted_tags}",
            )
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as response:
                    request = await response.json()
        except TimeoutError:
            return {}
        if not request:
            return {}
        return request

    @staticmethod
    def get_img_url(post):
        return post.get(
            "large_file_url", post.get("file_url", post.get("preview_file_url"))
        )


providers = {"rule34": R34, "danbooru": Danbooru}


class NSFW(commands.Cog, name="nsfw"):
    author = "googer_"

    def __init__(self, bot):
        self.bot = bot

    cmds = discord.SlashCommandGroup(
        "nsfw",
        "",
        name_localizations=localise("cog.nsfw.command_group.name"),
        description_localizations=localise("cog.nsfw.command_group.desc"),
    )

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.nsfw.commands.find.name"),
        description_localizations=localise("cog.nsfw.commands.find.desc"),
    )
    @commands.is_nsfw()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def find(
        self,
        ctx: discord.ApplicationContext,
        tags: discord.Option(
            str,
            name_localizations=localise("cog.nsfw.commands.find.options.tags.name"),
            description=localise(
                "cog.nsfw.commands.find.options.tags.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.nsfw.commands.find.options.tags.desc"
            ),
        ),
        provider: discord.Option(
            str,
            name_localizations=localise("cog.nsfw.commands.find.options.provider.name"),
            description=localise(
                "cog.nsfw.commands.find.options.provider.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.nsfw.commands.find.options.provider.desc"
            ),
            choices=list(providers.keys()),
        ) = "rule34",
    ):
        await ctx.response.defer()
        _provider = providers.get(provider)
        _tags = [tag.strip() for tag in tags.split(",")]
        _posts = await _provider.get_posts(_tags)
        if len(_posts) < 1:
            await ctx.followup.send(
                localise("cog.nsfw.answers.zero_returned", ctx.interaction.locale)
            )
            return
        post = {}
        while _provider.get_img_url(post) is None:
            post = random.choice(_posts)

        async with aiohttp.ClientSession() as session:
            status = await download_file(
                session, _provider.get_img_url(post), media=True
            )
            if status["error"]:
                await ctx.followup.send(status["error"])
                return
            dest = io.BytesIO(status["data"])
            file = discord.File(
                dest,
                filename=os.path.basename(
                    urllib.parse.urlparse(_provider.get_img_url(post)).path
                ),
            )
            await ctx.followup.send(file=file)

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.nsfw.commands.bomb.name"),
        description_localizations=localise("cog.nsfw.commands.bomb.desc"),
    )
    @commands.is_nsfw()
    @commands.cooldown(5, 10, commands.BucketType.user)
    async def bomb(
        self,
        ctx: discord.ApplicationContext,
        tags: discord.Option(
            str,
            name_localizations=localise("cog.nsfw.commands.bomb.options.tags.name"),
            description=localise(
                "cog.nsfw.commands.bomb.options.tags.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.nsfw.commands.bomb.options.tags.desc"
            ),
        ),
        provider: discord.Option(
            str,
            name_localizations=localise("cog.nsfw.commands.bomb.options.provider.name"),
            description=localise(
                "cog.nsfw.commands.bomb.options.provider.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.nsfw.commands.bomb.options.provider.desc"
            ),
            choices=list(providers.keys()),
        ) = "rule34",
    ):
        _provider = providers.get(provider)
        _tags = [tag.strip() for tag in tags.split(",")]

        await ctx.response.defer()

        _posts = await _provider.get_posts(_tags)
        if len(_posts) < 1:
            await ctx.followup.send(
                localise("cog.nsfw.answers.zero_returned", ctx.interaction.locale)
            )
            return
        posts = [random.choice(_posts) for _ in range(min(len(_posts), 10))]
        files = []
        async with aiohttp.ClientSession() as session:
            for post in posts:
                status = await download_file(
                    session, _provider.get_img_url(post), media=True
                )
                if status["error"]:
                    continue
                dest = io.BytesIO(status["data"])
                file = discord.File(
                    dest,
                    filename=os.path.basename(
                        urllib.parse.urlparse(_provider.get_img_url(post)).path
                    ),
                )
                files.append(file)

        await ctx.followup.send(files=files)


def setup(bot):
    bot.add_cog(NSFW(bot))
