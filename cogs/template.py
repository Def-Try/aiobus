import discord
from discord.ext import commands
from config import CONFIG
import json

class template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(template(bot))
