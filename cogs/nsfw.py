import discord
from discord.ext import commands
import requests
import random

from config import CONFIG
from localisation import localise
from localisation import DEFAULT_LOCALE


class Provider:
    def get_img_url(post): return post['url']
    def get_posts(tags): return {'url': 'http://example.com'}

class R34:
    def get_posts(tags):
        formatted_tags = ""
        for tag in tags:
            formatted_tags += tag
            formatted_tags += "+"
        if formatted_tags.endswith("+"): formatted_tags = formatted_tags[:-1]
        request = requests.get(
            'https://api.rule34.xxx/index.php?'
            'page=dapi&s=post&q=index&tags={}&limit=1000&pid={}&json=1'.format(
                formatted_tags, 0
            ),
            headers={"User-Agent": "Mozilla/5.0", "Host": "api.rule34.xxx", "Accept": "*/*"}
        )
        if not request.text: return {}
        return request.json()
    def get_img_url(post):
        return post['file_url']


providers = {'rule34': R34}


class NSFW(commands.Cog, name="template"):
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
    async def find(self, ctx: discord.ApplicationContext,
            tags: discord.Option(
                str,
                name_localizations=localise(
                    "cog.nsfw.commands.find.options.tags.name"
                ),
                description=localise(
                    "cog.nsfw.commands.find.options.tags.desc", DEFAULT_LOCALE
                ),
                description_localizations=localise(
                    "cog.nsfw.commands.find.options.tags.desc"
                ),
            ),
            provider: discord.Option(
                str,
                name_localizations=localise(
                    "cog.nsfw.commands.find.options.provider.name"
                ),
                description=localise(
                    "cog.nsfw.commands.find.options.provider.desc", DEFAULT_LOCALE
                ),
                description_localizations=localise(
                    "cog.nsfw.commands.find.options.provider.desc"
                ),
                choices=list(providers.keys()),
            )='rule34'
        ):
        _provider = providers.get(provider)
        _tags = [tag.strip() for tag in tags.split(',')]
        post = random.choice(_provider.get_posts(_tags))
        await ctx.respond(_provider.get_img_url(post))

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.nsfw.commands.bomb.name"),
        description_localizations=localise("cog.nsfw.commands.bomb.desc"),
    )
    @commands.is_nsfw()
    async def bomb(self, ctx: discord.ApplicationContext,
            tags: discord.Option(
                str,
                name_localizations=localise(
                    "cog.nsfw.commands.bomb.options.tags.name"
                ),
                description=localise(
                    "cog.nsfw.commands.bomb.options.tags.desc", DEFAULT_LOCALE
                ),
                description_localizations=localise(
                    "cog.nsfw.commands.bomb.options.tags.desc"
                ),
            ),
            provider: discord.Option(
                str,
                name_localizations=localise(
                    "cog.nsfw.commands.bomb.options.provider.name"
                ),
                description=localise(
                    "cog.nsfw.commands.bomb.options.provider.desc", DEFAULT_LOCALE
                ),
                description_localizations=localise(
                    "cog.nsfw.commands.bomb.options.provider.desc"
                ),
                choices=list(providers.keys()),
            )='rule34'
        ):
        _provider = providers.get(provider)
        _tags = [tag.strip() for tag in tags.split(',')]
        _posts = _provider.get_posts(_tags)
        posts = [random.choice(_posts) for _ in range(10)]
        await ctx.respond("\n".join([_provider.get_img_url(post) for post in posts]))


def setup(bot):
    bot.add_cog(NSFW(bot))
