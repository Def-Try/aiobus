import discord
from discord.ext import commands
from config import CONFIG
from localisation import localise
from tinydb import TinyDB, Query
import json
import time
import random
import string
import aiohttp

# interchat bans.
# michaai / UID 629999906429337600: opening, ending, and in general interacting with interchats.
#      reason: just a clown. spammed a bunch of NSFW links and got around ban with this thing.
interchat_bans = {
    "begin": [
         629999906429337600 # @michaai
    ],
    "end": [
         629999906429337600 # @michaai
    ],
    "info": [
         629999906429337600 # @michaai
    ],
    "address": [
         629999906429337600 # @michaai
    ],
    "send": [
         629999906429337600 # @michaai
    ]
}

class interchat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = TinyDB('databases/interchat.db')
        self.tdb = TinyDB('databases/interchat_tunnels.db')
        self.tunnels = []

    @commands.Cog.listener("on_ready")
    async def complete_init_interchat(self):

        async def fetch_message(channel, mid):
            try:
                return await channel.fetch_message(mid)
            except:
                return None

        for tunnel in self.tdb:
            self.tunnels.append({})
            rtunnel = self.tunnels[-1]
            rtunnel["out"] = self.bot.get_channel(tunnel["out"]) or self.bot.get_partial_messageable(tunnel["out"])
            rtunnel["in"] = self.bot.get_channel(tunnel["in"]) or self.bot.get_partial_messageable(tunnel["in"])
            rtunnel["whookless"] = tunnel["whookless"]
            if not tunnel["whookless"]:
                rtunnel["outwhook"] = await discord.Webhook.from_url(tunnel["outwhook"], session=aiohttp.ClientSession()).fetch()
                rtunnel["inwhook"] = await discord.Webhook.from_url(tunnel["inwhook"], session=aiohttp.ClientSession()).fetch()
            rtunnel["messages"] = list(filter(lambda x: x, [await fetch_message(rtunnel["out" if i[1] else "in"], i[0]) for i in tunnel["messages"]]))
            rtunnel["rmessages"] = list(filter(lambda x: x, [await fetch_message(rtunnel["out" if i[1] else "in"], i[0]) for i in tunnel["rmessages"]]))
            rtunnel["permanent"] = tunnel["permanent"]
            rtunnel["started"] = tunnel["started"]

    def get_address(self, channel):
        addrs = self.db.search(Query().chid == channel.id)
        if len(addrs) == 0: addr = None
        else: addr = addrs[0].get("address", None)
        if addr is None:
            while True:
                addr = self.generate_address()
                addrcs = self.db.search(Query().address == addr)
                if len(addrcs) == 0: break
            self.db.insert({"chid": channel.id, "address": addr, "guid": channel.guild.id if not isinstance(channel, discord.abc.PrivateChannel) and not isinstance(channel, discord.PartialMessageable) else -1})
        return addr

    def generate_address(self):
        c = (string.ascii_uppercase + string.digits)
        return "".join(random.choices(c, k=3))+"-"+"".join(random.choices(c, k=4))+"-"+"".join(random.choices(c, k=2))

    def address_string(self, channel):
        return f"[[ {channel.guild.name if not isinstance(channel, discord.abc.PrivateChannel) and not isinstance(channel, discord.PartialMessageable) else 'DM'}, {channel.name if not isinstance(channel, discord.abc.PrivateChannel) and not isinstance(channel, discord.PartialMessageable) else '???'}, {self.get_address(channel)} ]]"

    async def start_interserver(self, fromch, toch):
        for tunnel in self.tunnels:
            if tunnel["out"] == fromch:
                return False
            if tunnel["in"] == toch:
                return False
            if tunnel["out"] == toch:
                return False
            if tunnel["in"] == fromch:
                return False

        whookless = isinstance(fromch, discord.abc.PrivateChannel) or isinstance(toch, discord.abc.PrivateChannel) or isinstance(fromch, discord.PartialMessageable) or isinstance(toch, discord.PartialMessageable)
        self.tunnels.append({**{"out": fromch, "in": toch, 
            "messages": [], "rmessages": [], "permanent": False,
            "started": round(time.time()), "whookless": whookless}, **({
                "outwhook": await fromch.create_webhook(name="Outgoing interserver tunnel"),
                "inwhook":  await toch.create_webhook(name="Incoming interserver tunnel")
                } if not whookless else {})})
        self.tdb.insert({
            **{"in": toch.id, "out": fromch.id,
            "messages": [], "rmessages": [], "permanent": False,
            "started": round(time.time()), "whookless": whookless}, 
            **({"inwhook": self.tunnels[-1]["inwhook"].url, "outwhook": self.tunnels[-1]["outwhook"].url} if not whookless else {})}
            )
        return True

    async def end_interserver(self, tunnel):
        if not tunnel["whookless"]:
            await tunnel["outwhook"].delete()
            await tunnel["inwhook"].delete()
        q = Query()
        self.tdb.remove(q["in"] == tunnel["in"].id and q["out"] == tunnel["out"].id)

    async def update_interserver(self, tunnel):
        q = Query()
        self.tdb.update(
            {"messages": [[i.id, i.channel.id == tunnel["out"].id] for i in tunnel["messages"]], "rmessages": [[i.id, i.channel.id == tunnel["out"].id] for i in tunnel["rmessages"]]},
            q["in"] == tunnel["in"].id and q["out"] == tunnel["out"].id
            )


    @commands.Cog.listener("on_message")
    async def tunneling_onmsg(self, message):
        if message.author.id == self.bot.user.id or message.author.id in interchat_bans["send"]: return
        for itunnel in self.tunnels:
            if not itunnel["whookless"] and (message.author.id == itunnel["outwhook"].id or message.author.id == itunnel["inwhook"].id): return
            if message.channel.id == itunnel["out"].id:
                sticker_embeds = []
                ref_embed = None
                if message.reference:
                    ref_embed = discord.Embed(title="Replying to...", description=(message.reference.resolved.content if len(message.reference.resolved.content) < 30 else message.reference.resolved.content[:27]+"..."))
                    ref_embed.set_author(
                        name=(message.reference.resolved.author.name if isinstance(message.reference.resolved.author, discord.User) or not message.reference.resolved.author.nick else message.reference.resolved.author.nick),
                        icon_url=(message.reference.resolved.author.default_avatar.url if not message.reference.resolved.author.avatar.url else message.reference.resolved.author.avatar.url))

                for i in message.stickers:
                    sticker_embeds.append(discord.Embed(url=i.url))
                    sticker_embeds[-1].set_image(url=i.url)
                itunnel["messages"].append(
                    await (itunnel["inwhook"].send(message.content, 
                        username=(message.author.name if isinstance(message.author, discord.User) or not message.author.nick else message.author.nick),
                        avatar_url=(message.author.default_avatar.url if not message.author.avatar.url else message.author.avatar.url),
                        embeds=(message.embeds or []) + sticker_embeds + ([ref_embed] if ref_embed else []),
                        files=[await i.to_file() for i in message.attachments],
                        wait=True,
                        allowed_mentions=discord.AllowedMentions.none()
                        ) if not itunnel["whookless"] else 
                    itunnel["in"].send((message.author.name if isinstance(message.author, discord.User) or not message.author.nick else message.author.nick)+": "+message.clean_content,
                        embeds=(message.embeds or []) + sticker_embeds + ([ref_embed] if ref_embed else []),
                        files=[await i.to_file() for i in message.attachments]))
                    )
                itunnel["rmessages"].append(message)
                await self.update_interserver(itunnel)
                break
            if message.channel.id == itunnel["in"].id:
                sticker_embeds = []
                ref_embed = None
                if message.reference:
                    ref_embed = discord.Embed(title="Replying to...", description=(message.reference.resolved.content if len(message.reference.resolved.content) < 30 else message.reference.resolved.content[:27]+"..."))
                    ref_embed.set_author(
                        name=(message.reference.resolved.author.name if isinstance(message.reference.resolved.author, discord.User) or not message.reference.resolved.author.nick else message.reference.resolved.author.nick),
                        icon_url=(message.reference.resolved.author.default_avatar.url if not message.reference.resolved.author.avatar.url else message.reference.resolved.author.avatar.url))

                for i in message.stickers:
                    sticker_embeds.append(discord.Embed(url=i.url))
                    sticker_embeds[-1].set_image(url=i.url)
                itunnel["messages"].append(
                    await (itunnel["outwhook"].send(message.content, 
                        username=(message.author.name if isinstance(message.author, discord.User) or not message.author.nick else message.author.nick),
                        avatar_url=(message.author.default_avatar.url if not message.author.avatar.url else message.author.avatar.url),
                        embeds=(message.embeds or []) + sticker_embeds + ([ref_embed] if ref_embed else []),
                        files=[await i.to_file() for i in message.attachments],
                        wait=True,
                        allowed_mentions=discord.AllowedMentions.none()
                        ) if not itunnel["whookless"] else 
                    itunnel["out"].send((message.author.name if isinstance(message.author, discord.User) or not message.author.nick else message.author.nick)+": "+message.clean_content,
                        embeds=(message.embeds or []) + sticker_embeds + ([ref_embed] if ref_embed else []),
                        files=[await i.to_file() for i in message.attachments]))
                    )
                itunnel["rmessages"].append(message)
                await self.update_interserver(itunnel)
                break

    @commands.Cog.listener("on_message_edit")
    async def tunneling_onmsgedit(self, message_before, message):
        if message.author.id == self.bot.user.id or message.author.id in interchat_bans["send"]: return
        for itunnel in self.tunnels:
            if not itunnel["whookless"] and (message.author.id == itunnel["outwhook"].id or message.author.id == itunnel["inwhook"].id): return
            if message.channel == itunnel["out"]:
                sticker_embeds = []
                ref_embed = None
                if message.reference:
                    ref_embed = discord.Embed(title="Replying to...", description=(message.reference.resolved.content if len(message.reference.resolved.content) < 30 else message.reference.resolved.content[:27]+"..."))
                    ref_embed.set_author(
                        name=(message.reference.resolved.author.name if isinstance(message.reference.resolved.author, discord.User) or not message.reference.resolved.author.nick else message.reference.resolved.author.nick),
                        icon_url=(message.reference.resolved.author.default_avatar.url if not message.reference.resolved.author.avatar.url else message.reference.resolved.author.avatar.url))

                for i in message.stickers:
                    sticker_embeds.append(discord.Embed(url=i.url))
                    sticker_embeds[-1].set_image(url=i.url)
                if not itunnel["whookless"]:
                    itunnel["messages"][itunnel["rmessages"].index(message_before)] = await itunnel["inwhook"].edit_message(itunnel["messages"][itunnel["rmessages"].index(message_before)].id,
                            content=message.content, 
                            embeds=(message.embeds or []) + sticker_embeds + ([ref_embed] if ref_embed else []),
                            files=[await i.to_file() for i in message.attachments],
                            allowed_mentions=discord.AllowedMentions.none()
                        )
                else:
                    itunnel["messages"][itunnel["rmessages"].index(message_before)] = itunnel["messages"][itunnel["rmessages"].index(message_before)].edit((message.author.name if isinstance(message.author, discord.User) or not message.author.nick else message.author.nick)+": "+message.clean_content,
                        embeds=(message.embeds or []) + sticker_embeds + ([ref_embed] if ref_embed else []),
                        files=[await i.to_file() for i in message.attachments])
                itunnel["rmessages"][itunnel["rmessages"].index(message_before)] = message
                await self.update_interserver(itunnel)
                break
            if message.channel == itunnel["in"]:
                sticker_embeds = []
                ref_embed = None
                if message.reference:
                    ref_embed = discord.Embed(title="Replying to...", description=(message.reference.resolved.content if len(message.reference.resolved.content) < 30 else message.reference.resolved.content[:27]+"..."))
                    ref_embed.set_author(
                        name=(message.reference.resolved.author.name if isinstance(message.reference.resolved.author, discord.User) or not message.reference.resolved.author.nick else message.reference.resolved.author.nick),
                        icon_url=(message.reference.resolved.author.default_avatar.url if not message.reference.resolved.author.avatar.url else message.reference.resolved.author.avatar.url))

                for i in message.stickers:
                    sticker_embeds.append(discord.Embed(url=i.url))
                    sticker_embeds[-1].set_image(url=i.url)
                if not itunnel["whookless"]:
                    itunnel["messages"][itunnel["rmessages"].index(message_before)] = await itunnel["outwhook"].edit_message(itunnel["messages"][itunnel["rmessages"].index(message_before)].id,
                            content=message.content, 
                            embeds=(message.embeds or []) + sticker_embeds + ([ref_embed] if ref_embed else []),
                            files=[await i.to_file() for i in message.attachments],
                            allowed_mentions=discord.AllowedMentions.none()
                        )
                else:
                    itunnel["messages"][itunnel["rmessages"].index(message_before)] = itunnel["messages"][itunnel["rmessages"].index(message_before)].edit((message.author.name if isinstance(message.author, discord.User) or not message.author.nick else message.author.nick)+": "+message.clean_content,
                        embeds=(message.embeds or []) + sticker_embeds + ([ref_embed] if ref_embed else []),
                        files=[await i.to_file() for i in message.attachments])
                itunnel["rmessages"][itunnel["rmessages"].index(message_before)] = message
                await self.update_interserver(itunnel)
                break

    @commands.Cog.listener("on_message_delete")
    async def tunneling_onmsgdel(self, message):
        if message.author.id == self.bot.user.id or message.author.id in interchat_bans["send"]: return
        for itunnel in self.tunnels:
            if not itunnel["whookless"] and (message.author.id == itunnel["outwhook"].id or message.author.id == itunnel["inwhook"].id): return
            if message.channel == itunnel["out"]:
                await itunnel["messages"][itunnel["rmessages"].index(message)].delete()
                itunnel["messages"].pop(itunnel["rmessages"].index(message))
                itunnel["rmessages"].pop(itunnel["rmessages"].index(message))
                await self.update_interserver(itunnel)
                break
            if message.channel == itunnel["in"]:
                await itunnel["messages"][itunnel["rmessages"].index(message)].delete()
                itunnel["messages"].pop(itunnel["rmessages"].index(message))
                itunnel["rmessages"].pop(itunnel["rmessages"].index(message))
                await self.update_interserver(itunnel)
                break

    cmds = discord.SlashCommandGroup("interchat", "",
        name_localizations=localise("cog.interchat.command_group.name"),
        description_localisations=localise("cog.interchat.command_group.desc"))

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.interchat.commands.begin.name"),
        description_localisations=localise("cog.interchat.commands.begin.desc"))
    async def begin(self, ctx: discord.ApplicationContext, address: str):
        if ctx.author.id in interchat_bans["begin"]:
            await ctx.respond(localise("generic.banned_from_command", ctx.interaction.locale))
            return
        addrs = self.db.search(Query().address == address)
        if len(addrs) == 0:
            await ctx.respond(localise("cog.interchat.answers.begin.notfound", ctx.interaction.locale))
            return
        chid = addrs[0]["chid"]
        guid = addrs[0]["guid"]
        channel = self.bot.get_channel(chid) or self.bot.get_partial_messageable(chid)
        if channel == ctx.channel:
            await ctx.respond("Unable to open interchat tunnel to the same channel you are in.", ephemeral=True)
        await ctx.response.defer(ephemeral=True)
        if await self.start_interserver(ctx.channel, channel):
            await channel.send(f"# Incoming interchat communication channel.\nTunnel opened - `{self.get_address(ctx.channel)}` requested connection.\n{ctx.channel.guild.name if not isinstance(ctx.channel, discord.abc.PrivateChannel) and not isinstance(ctx.channel, discord.PartialMessageable) else 'DM'} - {ctx.channel.name if not isinstance(ctx.channel, discord.abc.PrivateChannel) and not isinstance(ctx.channel, discord.PartialMessageable) else ctx.channel.recipient.name}")
            await ctx.channel.send(f"# Outgoing interchat communication channel.\nTunnel opened - connection requested to `{self.get_address(channel)}`.\n{channel.guild.name if not isinstance(channel, discord.abc.PrivateChannel) and not isinstance(channel, discord.PartialMessageable) else 'DM'} - {channel.name if not isinstance(channel, discord.abc.PrivateChannel) and not isinstance(channel, discord.PartialMessageable) else '???'}")
            await ctx.followup.send("OK", ephemeral=True)
        else:
            await ctx.followup.send("Tunnel failed to open - there is already online connection using that address.", ephemeral=True)

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.interchat.commands.end.name"),
        description_localisations=localise("cog.interchat.commands.end.desc"))
    async def end(self, ctx: discord.ApplicationContext):
        if ctx.author.id in interchat_bans["end"]:
            await ctx.respond(localise("generic.banned_from_command", ctx.interaction.locale))
            return
        for i, tunnel in enumerate(self.tunnels):
            if ctx.channel == tunnel["in"]:
                if tunnel["permanent"]:
                    await ctx.respond("Unable to close permanent tunnel. Contact googer_ if you want to move or close this tunnel.")
                    return
                await ctx.respond("OK", ephemeral=True)
                await ctx.channel.send(f"# Incoming interchat communication channel ended by this side.\nTunnel closed. {self.address_string(tunnel['out'])} -> {self.address_string(tunnel['in'])}({localise('generic.here', ctx.interaction.locale)})")
                await tunnel["out"].send(f"# Outgoing interchat communication channel ended by receiver side.\nTunnel closed. {self.address_string(tunnel['out'])}({localise('generic.here', ctx.interaction.locale)}) -> {self.address_string(tunnel['in'])}")
                await self.end_interserver(tunnel)
                self.tunnels.pop(i)
                return
            if ctx.channel == tunnel["out"]:
                if tunnel["permanent"]:
                    await ctx.respond("Unable to close permanent tunnel. Contact googer_ if you want to move or close this tunnel.")
                    return
                await ctx.respond("OK", ephemeral=True)
                await ctx.channel.send(f"# Outgoing interchat communication channel ended by this side.\nTunnel closed. {self.address_string(tunnel['out'])}({localise('generic.here', ctx.interaction.locale)}) -> {self.address_string(tunnel['in'])}")
                await tunnel["in"].send(f"# Incoming interchat communication channel ended by opener side.\nTunnel closed. {self.address_string(tunnel['out'])} -> {self.address_string(tunnel['in'])}({localise('generic.here', ctx.interaction.locale)})")
                await self.end_interserver(tunnel)
                self.tunnels.pop(i)
                return
        await ctx.respond("No opened tunnel for this channel has been found", ephemeral=True)



    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.interchat.commands.address.name"),
        description_localisations=("cog.interchat.commands.address.desc"))
    async def address(self, ctx: discord.ApplicationContext):
        if ctx.author.id in interchat_bans["address"]:
            await ctx.respond(localise("generic.banned_from_command", ctx.interaction.locale))
            return
        await ctx.respond(localise("cog.interchat.answers.getaddress", ctx.interaction.locale).format(address=self.get_address(ctx.channel)))

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.interchat.commands.info.name"),
        description_localisations=("cog.interchat.commands.info.desc"))
    async def info(self, ctx: discord.ApplicationContext):
        if ctx.author.id in interchat_bans["info"]:
            await ctx.respond(localise("generic.banned_from_command", ctx.interaction.locale))
            return

        this_tunnel = None
        for i, tunnel in enumerate(self.tunnels):
            if ctx.channel == tunnel["in"] or ctx.channel == tunnel["out"]:
                this_tunnel = tunnel
                break
        if not this_tunnel:
            await ctx.respond(localise("cog.interchat.answers.getinfo.offline", ctx.interaction.locale))
            return
        await ctx.respond(localise("cog.interchat.answers.getinfo.online", ctx.interaction.locale).format(
            started=f"<t:{this_tunnel['started']}:R>",
            address_out=self.address_string(tunnel["out"]),
            out_here=(f"({localise('generic.here', ctx.interaction.locale)})" if ctx.channel == tunnel["out"] else ""),
            address_in=self.address_string(tunnel["in"]),
            in_here=(f"({localise('generic.here', ctx.interaction.locale)})" if ctx.channel == tunnel["in"] else ""),
            permanent=(localise("generic.yes", ctx.interaction.locale) if tunnel["permanent"] else localise("generic.no", ctx.interaction.locale))
        ))

def setup(bot):
    bot.add_cog(interchat(bot))
