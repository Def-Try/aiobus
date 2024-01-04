import discord
from discord.ext import commands
from nekosbest import Client, Result
from config import CONFIG
from localisation import localise

import json

nekosbest_client = Client()

categories = ['baka', 'bite', 'blush', 'bored', 'cry', 'cuddle', 
              'dance', 'facepalm', 'feed', 'happy', 'highfive', 
              'hug', 'kiss', 'laugh', 'neko', 'pat', 'poke', 
              'pout', 'shrug', 'slap', 'sleep', 'smile', 
              'smug', 'stare', 'think', 'thumbsup', 'tickle', 
              'wave', 'wink', 'kitsune', 'waifu', 'handhold', 
              'kick', 'punch', 'shoot', 'husbando', 'yeet', 
              'nod', 'nom', 'nope', 'handshake', 'lurk', 
              'peck', 'yawn']

class gif_related(commands.Cog):
    author = "googer_"

    def __init__(self, bot):
        self.bot = bot

    gif_cmds = discord.SlashCommandGroup("gif", "",
        name_localizations=localise("cog.gif_related.command_group.name"),
        description_localizations=localise("cog.gif_related.command_group.desc"))

    @gif_cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.gif_related.commands.findgif.name"),
        description_localizations=localise("cog.gif_related.commands.findgif.desc"))
    async def findgif(self, ctx: discord.ApplicationContext, category: discord.Option(str)):
        locale = ctx.interaction.locale
        if category not in categories:
            await ctx.respond(localise("cog.gif_related.answers.findgif.invalid_category", locale).format(categories=", ".join(categories)))
            return
        result = await nekosbest_client.get_image(category, 1)
        embed = discord.Embed(
            title=localise("cog.gif_related.answers.findgif.title", locale),
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(gif_related(bot))
