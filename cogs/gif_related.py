import discord
from discord.ext import commands

from nekosbest import Client, Result

import json
with open("config.cfg", 'r') as f:
    CONFIG = json.loads(f.read())

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
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=CONFIG["g_ids"], name="гифка", description="Найти гифку по одной из нескольких категорий." + \
                                                                                 "Работает с помощью nekos.best API.")
    async def find_gif(self, ctx: discord.ApplicationContext, category: discord.Option(str)):
        if category not in categories:
            await ctx.respond(f"Неверная категория: должна быть одной из следующих: {', '.join(categories)}")
            return
        result = await nekosbest_client.get_image(category, 1)
        embed = discord.Embed(
            title="Гифка",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(gif_related(bot))
