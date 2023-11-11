import discord
from discord.ext import commands

import json
with open("config.cfg", 'r') as f:
    CONFIG = json.loads(f.read())

class template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(template(bot))
