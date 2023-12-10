import discord
from discord.ext import commands, tasks
import datetime
from localisation import LOCALISATIONS
import json
from tinydb import TinyDB, Query
from config import CONFIG
import re

OFFTOPIC_PREFIXES = ["//", "(("]
ACTION_INDICATORS = [r"\*\*\*", r"\*\*", r"\*"]
AWAY_KEYWORDS     = ["ушёл", "ушел", "телепортировался", "пропал"
                     "went away", "teleports", "teleported", "disappeared",
                      "fissled away"]

class rp_utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = TinyDB('databases/rputils.db')

        q = Query()
        self.rp_channels = self.db.search(q.type == "RP_CHANNEL").copy()

        self.away_from_keyboard_checks.start()

    rpu = discord.SlashCommandGroup("rp_utils", "",
        name_localizations=LOCALISATIONS["cog"]["rp_utils"]["command_group"]["name"],
        description_localisations=LOCALISATIONS["cog"]["rp_utils"]["command_group"]["desc"])

    @rpu.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["rp_utils"]["commands"]["clean_offtopic"]["name"],
        description_localisations=LOCALISATIONS["cog"]["rp_utils"]["commands"]["clean_offtopic"]["desc"])
    async def clean_offtopic(self, ctx: discord.ApplicationContext):
        await ctx.response.defer()
        locale = ctx.interaction.locale
        messages = list()
        async for message in ctx.channel.history(limit=1000):
            if (any([message.content.startswith(offtopic_start) for offtopic_start in OFFTOPIC_PREFIXES])
                    and datetime.datetime.now(message.created_at.tzinfo) - message.created_at <= datetime.timedelta(days=14) and not message.pinned):
                messages.append(message)
        await ctx.followup.send(
            LOCALISATIONS["cog"]["rp_utils"]["answers"]["clean_offtopic"]["message"][
                ('_1' 
                    if len(messages) == 1 or len(messages) % 10 == 1 else
                '_2..4'
                    if len(messages) % 10 in (2, 3, 4) else
                '_5..9+0'
                    if len(messages) % 10 in (5, 6, 7, 8, 9, 0) else
                'HOWTHEFUCK')].get(locale, f"ERR: LOCALE NOT FOUND: {locale}").format(x=len(messages)))
        for i in range(0, len(messages), 100):
            await ctx.channel.delete_messages(messages[i:i+100], reason=LOCALISATIONS["cog"]["rp_utils"]["answers"]["clean_offtopic"]["audit"].get(locale, f"ERR: LOCALE NOT FOUND: {locale}").format(prefixes=OFFTOPIC_PREFIXES))

    @rpu.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["rp_utils"]["commands"]["init_rp_channel"]["name"],
        description_localisations=LOCALISATIONS["cog"]["rp_utils"]["commands"]["init_rp_channel"]["desc"])
    async def init_rp_channel(self, ctx: discord.ApplicationContext):
        self.db.insert({"type": "RP_CHANNEL", "id": ctx.channel.id})
        self.rp_channels.append({"type": "RP_CHANNEL", "id": ctx.channel.id})
        await ctx.respond("РП Канал добавлен.")

    @tasks.loop(seconds=5)
    async def away_from_keyboard_checks(self):
        def parse_actions(text):
            actions = []
            for act_mark in ACTION_INDICATORS:
                actions += re.findall(r"(?<="+act_mark+r").*?(?="+act_mark+r")", text)[0::2]
                for act in actions:
                    text = text.replace(act_mark+act+act_mark, "")
            return actions


        for channel in self.rp_channels:
            in_channel = []
            went_away = []
            try:
                ch = await self.bot.fetch_channel(channel["id"])
            except AttributeError: # bot isn't started yet, ignore
                continue
            for message in reversed(await ch.history(limit=100).flatten()):
                if any([message.content.startswith(offtopic_start) for offtopic_start in OFFTOPIC_PREFIXES]): continue
                if message.author == self.bot.user:
                    for person in in_channel:
                        if message.content == LOCALISATIONS["cog"]["rp_utils"]["answers"]["user_afk"][CONFIG["locale"]].format(user=f"<@{person}>"):
                            went_away.append(message.mentions[0].id)
                            continue
                    continue
                if not message.author.id in in_channel: in_channel.append(message.author.id)
                if datetime.datetime.now(message.created_at.tzinfo) - message.created_at <= datetime.timedelta(minutes=5):
                    went_away.append(message.author.id)
                    continue
                if any([away_act in ";".join(parse_actions(message.content)) for away_act in AWAY_KEYWORDS]):
                    went_away.append(message.author.id)
                    continue
                if message.author.id in went_away:
                    while message.author.id in went_away:
                        went_away.pop(went_away.index(message.author.id))
            if sorted(in_channel) == sorted(went_away): continue
            for person in in_channel:
                if person in went_away: continue
                await ch.send(LOCALISATIONS["cog"]["rp_utils"]["answers"]["user_afk"][CONFIG["locale"]].format(user=f"<@{person}>"))


def setup(bot):
    bot.add_cog(rp_utils(bot))
