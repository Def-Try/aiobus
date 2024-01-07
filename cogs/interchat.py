import discord
from discord.ext import commands
from config import CONFIG
from localisation import localise, DEFAULT_LOCALE
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

    "address_hub": [
         629999906429337600 # @michaai
    ],
    "bind": [
         629999906429337600 # @michaai
    ],
    "unbind": [
         629999906429337600 # @michaai
    ],
    "destroy_hub": [
         629999906429337600 # @michaai
    ],

    "send": [
         629999906429337600 # @michaai
    ]
}

class interchat(commands.Cog, name="interchat"):
    author = "googer_ & minemaster_"

    def __init__(self, bot):
        self.bot = bot
        self.db = TinyDB('databases/interchat.db')
        self.tdb = TinyDB('databases/interchat_tunnels.db')
        self.hdb = TinyDB('databases/interchat_hubs.db')
        self.tunnels = []
        self.hubs = []

    async def unload(self):
        pass

    @commands.Cog.listener("on_ready")
    async def complete_init_interchat(self):

        async def fetch_message(channel, mid):
            try:
                return await channel.fetch_message(mid)
            except:
                return None

        for tunnel in self.tdb:
            rtunnel = {}
            rtunnel["out"] = self.bot.get_channel(tunnel["out"]) or self.bot.get_partial_messageable(tunnel["out"])
            rtunnel["in"] = self.bot.get_channel(tunnel["in"]) or self.bot.get_partial_messageable(tunnel["in"])
            rtunnel["whookless"] = tunnel["whookless"]
            if not tunnel["whookless"]:
                rtunnel["outwhook"] = await discord.Webhook.from_url(tunnel["outwhook"], session=self.bot.http._HTTPClient__session).fetch()
                rtunnel["inwhook"] = await discord.Webhook.from_url(tunnel["inwhook"], session=self.bot.http._HTTPClient__session).fetch()
            rtunnel["messages"] = list(filter(lambda x: x, [await fetch_message(rtunnel["out" if i[1] else "in"], i[0]) for i in tunnel["messages"]]))
            rtunnel["rmessages"] = list(filter(lambda x: x, [await fetch_message(rtunnel["out" if i[1] else "in"], i[0]) for i in tunnel["rmessages"]]))
            rtunnel["permanent"] = tunnel["permanent"]
            rtunnel["started"] = tunnel["started"]
            rtunnel["hub_addr"] = tunnel["hub_addr"]
            self.tunnels.append(rtunnel)

    def get_address(self, channel):
        addrs = self.db.search(Query().chid == channel.id)
        if len(addrs) == 0: addr = None
        else: addr = addrs[0].get("address", None)
        if addr is None:
            while True:
                addr = self.generate_address()
                addrcs1 = self.db.search(Query().address == addr)
                addrcs2 = self.hdb.search(Query().address == addr)
                if len(addrcs1) == 0 and len(addrcs2) == 0: break
            self.db.insert({"chid": channel.id, "address": addr, "guid": channel.guild.id if not isinstance(channel, discord.abc.PrivateChannel) and not isinstance(channel, discord.PartialMessageable) else -1})
        return addr

    def get_hub(self, channel=None, addr=None, create=True):
        if addr is not None:
            chns = self.hdb.search(Query().address == addr)
            if len(chns) == 0: addr = None
            else: addr = chns[0].get("address", None)
        if channel is not None:
            addrs = self.hdb.search(Query().host == channel.id)
            if len(addrs) == 0: addr = None
            else: addr = addrs[0].get("address", None)
        if addr is None and create:
            while True:
                addr = self.generate_address()
                addrcs1 = self.db.search(Query().address == addr)
                addrcs2 = self.hdb.search(Query().address == addr)
                if len(addrcs1) == 0 and len(addrcs2) == 0: break
            self.hdb.insert({"channels": [], "address": addr, "host": channel.id})
        if addr is None and not create: return None
        hubs = self.hdb.search(Query().address == addr)
        return hubs[0]

    def generate_address(self):
        c = (string.ascii_uppercase + string.digits)
        return "".join(random.choices(c, k=3))+"-"+"".join(random.choices(c, k=4))+"-"+"".join(random.choices(c, k=2))

    def address_string(self, channel):
        return f"`{channel.guild.name if not isinstance(channel, discord.abc.PrivateChannel) and not isinstance(channel, discord.PartialMessageable) else 'DM'}, {channel.name if not isinstance(channel, discord.abc.PrivateChannel) and not isinstance(channel, discord.PartialMessageable) else '???'}`, `{self.get_address(channel)}`"

    def address_string_hub(self, channel):
        return f"`{channel.guild.name if not isinstance(channel, discord.abc.PrivateChannel) and not isinstance(channel, discord.PartialMessageable) else 'DM'}, {channel.name if not isinstance(channel, discord.abc.PrivateChannel) and not isinstance(channel, discord.PartialMessageable) else '???'}`, `{self.get_hub(channel=channel)['address']}`"

    async def start_interchat(self, fromch, toch, hub=None):
        outwhook = None
        inwhook = None
        
        whookless = isinstance(fromch, discord.abc.PrivateChannel) or isinstance(toch, discord.abc.PrivateChannel) or isinstance(fromch, discord.PartialMessageable) or isinstance(toch, discord.PartialMessageable)

        for tunnel in self.tunnels:
            if tunnel["out"] == fromch and not hub:
                return False
            elif tunnel["out"] == fromch and not whookless:
                outwhook = tunnel["outwhook"]
            if tunnel["in"] == toch and not hub:
                return False
            elif tunnel["in"] == toch and not whookless:
                inwhook = tunnel["inwhook"]
            if tunnel["out"] == toch and not hub:
                return False
            elif tunnel["out"] == toch and not whookless:
                outwhook = tunnel["outwhook"]
            if tunnel["in"] == fromch and not hub:
                return False
            elif tunnel["in"] == fromch and not whookless:
                inwhook = tunnel["inwhook"]

        if not whookless and not outwhook:
            outwhook = await fromch.create_webhook(name="Outgoing interchat tunnel")
        if not whookless and not inwhook:
            inwhook = await toch.create_webhook(name="Incoming interchat tunnel")

        self.tunnels.append({**{"out": fromch, "in": toch, 
            "messages": [], "rmessages": [], "permanent": False,
            "started": round(time.time()), "hub_addr": hub, "whookless": whookless}, **({
                "outwhook": outwhook,
                "inwhook":  inwhook
                } if not whookless else {})})
        self.tdb.insert({
            **{"in": toch.id, "out": fromch.id,
            "messages": [], "rmessages": [], "permanent": False,
            "started": round(time.time()), "whookless": whookless, "hub_addr": hub}, 
            **({"inwhook": self.tunnels[-1]["inwhook"].url, "outwhook": self.tunnels[-1]["outwhook"].url} if not whookless else {})}
            )
        return True

    async def bind_interchat_hub(self, hub_addr, channel):
        hub = self.get_hub(addr=hub_addr)
        if channel.id in hub["channels"]: return -1
        if channel.id == hub["host"]: return -2
        if self.get_hub(channel=channel, create=False): -2
        if await self.start_interchat(channel, self.bot.get_channel(hub["host"]), hub_addr):
            for channelid in hub["channels"]:
                await self.start_interchat(channel, self.bot.get_channel(channelid), hub_addr)
            self.hdb.update({"channels": hub["channels"] + [channel.id]}, Query().address == hub_addr)
            return 1
        else:
            return -3

    async def end_interchat(self, tunnel):
        if not tunnel["whookless"] and not tunnel["hub_addr"]:
            await tunnel["outwhook"].delete()
            await tunnel["inwhook"].delete()
        elif not tunnel["whookless"] and tunnel["hub_addr"]:
            hub = self.get_hub(addr=tunnel["hub_addr"])
            if len(hub["channels"]) == 1:
                await tunnel["outwhook"].delete()
                await tunnel["inwhook"].delete()
        q = Query()
        self.tdb.remove(q["in"] == tunnel["in"].id and q["out"] == tunnel["out"].id and q["hub_addr"] == tunnel["hub_addr"])
        self.tunnels.pop(self.tunnels.index(tunnel))

    async def unbind_interchat_hub(self, hub_addr, channel):
        hub = self.get_hub(addr=hub_addr)
        if channel.id not in hub["channels"]: return -1
        if channel.id == hub["host"]: return -2
        for tunnel in filter(lambda tun: (tun["in"].id == channel.id or tun["out"].id == channel.id) and tun["hub_addr"] == hub_addr, self.tunnels):
            await self.end_interchat(tunnel)
        self.hdb.update({"channels": list(filter(lambda ch: ch != channel.id, hub["channels"]))}, Query().address == hub_addr)
        return 1

    async def update_interchat(self, tunnel):
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
            if message.channel.id == itunnel["out"].id or message.channel.id == itunnel["in"].id:
                sticker_embeds = []
                ref_embed = None
                if message.reference:
                    ref_embed = discord.Embed(title=localise("cog.interchat.answers.reply", DEFAULT_LOCALE), description=(message.reference.resolved.content if len(message.reference.resolved.content) < 30 else message.reference.resolved.content[:27]+"..."))
                    ref_embed.set_author(
                        name=(message.reference.resolved.author.name if isinstance(message.reference.resolved.author, discord.User) or not message.reference.resolved.author.nick else message.reference.resolved.author.nick),
                        icon_url=(message.reference.resolved.author.default_avatar.url if not message.reference.resolved.author.avatar.url else message.reference.resolved.author.avatar.url))

                for i in message.stickers:
                    sticker_embeds.append(discord.Embed(url=i.url))
                    sticker_embeds[-1].set_image(url=i.url)
                itunnel["messages"].append(
                    await (itunnel["inwhook" if message.channel.id == itunnel["out"].id else "outwhook"].send(message.content,
                        username=(message.author.name if isinstance(message.author, discord.User) or not message.author.nick else message.author.nick)+(((" / "+self.address_string(message.channel)) if itunnel["hub_addr"] else "")),
                        avatar_url=(message.author.default_avatar.url if not message.author.avatar.url else message.author.avatar.url),
                        embeds=(message.embeds or []) + sticker_embeds + ([ref_embed] if ref_embed else []),
                        files=[await i.to_file() for i in message.attachments],
                        wait=True,
                        allowed_mentions=discord.AllowedMentions.none()
                        ) if not itunnel["whookless"] else 
                    itunnel["in" if message.channel.id == itunnel["out"].id else "out"].send((message.author.name if isinstance(message.author, discord.User) or not message.author.nick else message.author.nick)+(((" / "+self.address_string(message.channel)) if itunnel["hub_addr"] else ""))+": "+message.clean_content,
                        embeds=(message.embeds or []) + sticker_embeds + ([ref_embed] if ref_embed else []),
                        files=[await i.to_file() for i in message.attachments]))
                    )
                itunnel["rmessages"].append(message)
                await self.update_interchat(itunnel)

    @commands.Cog.listener("on_message_edit")
    async def tunneling_onmsgedit(self, message_before, message):
        if message.author.id == self.bot.user.id or message.author.id in interchat_bans["send"]: return
        for itunnel in self.tunnels:
            if not itunnel["whookless"] and (message.author.id == itunnel["outwhook"].id or message.author.id == itunnel["inwhook"].id): return
            if message.channel.id == itunnel["out"].id or message.channel.id == itunnel["in"].id:
                sticker_embeds = []
                ref_embed = None
                if message.reference:
                    ref_embed = discord.Embed(title=localise("cog.interchat.answers.reply", DEFAULT_LOCALE), description=(message.reference.resolved.content if len(message.reference.resolved.content) < 30 else message.reference.resolved.content[:27]+"..."))
                    ref_embed.set_author(
                        name=(message.reference.resolved.author.name if isinstance(message.reference.resolved.author, discord.User) or not message.reference.resolved.author.nick else message.reference.resolved.author.nick),
                        icon_url=(message.reference.resolved.author.default_avatar.url if not message.reference.resolved.author.avatar.url else message.reference.resolved.author.avatar.url))

                for i in message.stickers:
                    sticker_embeds.append(discord.Embed(url=i.url))
                    sticker_embeds[-1].set_image(url=i.url)
                if not itunnel["whookless"]:
                    itunnel["messages"][itunnel["rmessages"].index(message_before)] = await itunnel["inwhook" if message.channel.id == itunnel["out"] else "outwhook"].edit_message(itunnel["messages"][itunnel["rmessages"].index(message_before)].id,
                            content=message.content,
                            embeds=(message.embeds or []) + sticker_embeds + ([ref_embed] if ref_embed else []),
                            files=[await i.to_file() for i in message.attachments],
                            allowed_mentions=discord.AllowedMentions.none()
                        )
                else:
                    itunnel["messages"][itunnel["rmessages"].index(message_before)] = itunnel["messages"][itunnel["rmessages"].index(message_before)].edit((message.author.name if isinstance(message.author, discord.User) or not message.author.nick else message.author.nick)+(((" / "+self.address_string(message.channel)) if itunnel["hub_addr"] else ""))+": "+message.clean_content,
                        embeds=(message.embeds or []) + sticker_embeds + ([ref_embed] if ref_embed else []),
                        files=[await i.to_file() for i in message.attachments])
                itunnel["rmessages"][itunnel["rmessages"].index(message_before)] = message
                await self.update_interchat(itunnel)

    @commands.Cog.listener("on_message_delete")
    async def tunneling_onmsgdel(self, message):
        if message.author.id == self.bot.user.id or message.author.id in interchat_bans["send"]: return
        for itunnel in self.tunnels:
            if not itunnel["whookless"] and (message.author.id == itunnel["outwhook"].id or message.author.id == itunnel["inwhook"].id): return
            if message.channel.id == itunnel["out"].id or message.channel.id == itunnel["in"].id:
                await itunnel["messages"][itunnel["rmessages"].index(message)].delete()
                itunnel["messages"].pop(itunnel["rmessages"].index(message))
                itunnel["rmessages"].pop(itunnel["rmessages"].index(message))
                await self.update_interchat(itunnel)

    cmds = discord.SlashCommandGroup("interchat", "",
        name_localizations=localise("cog.interchat.command_group.name"),
        description_localizations=localise("cog.interchat.command_group.desc"))

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.interchat.commands.address_hub.name"),
        description_localizations=localise("cog.interchat.commands.address_hub.desc"))
    async def address_hub(self, ctx: discord.ApplicationContext):
        if ctx.author.id in interchat_bans["address_hub"]:
            await ctx.respond(localise("generic.banned_from_command", ctx.interaction.locale), ephemeral=True)
            return
        await ctx.respond(localise("cog.interchat.answers.getaddresshub", ctx.interaction.locale).format(address=self.get_hub(channel=ctx.channel)["address"]))

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.interchat.commands.bind.name"),
        description_localizations=localise("cog.interchat.commands.bind.desc"))
    async def bind(self, ctx: discord.ApplicationContext, address: discord.Option(str,
            name_localizations=localise("cog.interchat.commands.bind.options.address.name"),
            description=localise("cog.interchat.commands.bind.options.address.desc", DEFAULT_LOCALE),
            description_localizations=localise("cog.interchat.commands.bind.options.address.desc"),
        )):
        if ctx.author.id in interchat_bans["bind"]:
            await ctx.respond(localise("generic.banned_from_command", ctx.interaction.locale), ephemeral=True)
            return
        await ctx.response.defer(ephemeral=True)
        if not self.get_hub(addr=address, create=False):
            await ctx.respond(localise("cog.interchat.answers.bind.not_found", ctx.interaction.locale), ephemeral=True)
            return
        result = await self.bind_interchat_hub(address, ctx.channel)
        if result == 1:
            await ctx.followup.send(localise("cog.interchat.answers.bind.success", ctx.interaction.locale))

            hub = self.get_hub(addr=address)

            embed = discord.Embed()
            embed.title = localise("cog.interchat.answers.bind.incoming", DEFAULT_LOCALE)
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.started", DEFAULT_LOCALE), value=f"<t:{round(time.time())}:F>")
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.our_side", DEFAULT_LOCALE), value=localise("cog.interchat.answers.info.receiver_side", DEFAULT_LOCALE))
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.hub.incoming_to", DEFAULT_LOCALE), value=self.address_string_hub(self.bot.get_channel(hub["host"])))
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.outgoing_from", DEFAULT_LOCALE), value=self.address_string(ctx.channel))
            embed.color = discord.Color.green()
            await self.bot.get_channel(hub["host"]).send(embed=embed)
            for channel in hub["channels"]:
                if channel == ctx.channel.id: continue
                await self.bot.get_channel(channel).send(embed=embed)

            embed = discord.Embed()
            embed.title = localise("cog.interchat.answers.bind.outgoing", DEFAULT_LOCALE)
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.started", DEFAULT_LOCALE), value=f"<t:{round(time.time())}:F>")
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.our_side", DEFAULT_LOCALE), value=localise("cog.interchat.answers.info.opener_side", DEFAULT_LOCALE))
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.hub.incoming_to", DEFAULT_LOCALE), value=self.address_string_hub(self.bot.get_channel(hub["host"])))
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.outgoing_from", DEFAULT_LOCALE), value=self.address_string(ctx.channel))
            embed.color = discord.Color.green()
            await ctx.channel.send(embed=embed)

            return
        if result == -1:
            await ctx.followup.send(localise("cog.interchat.answers.bind.already_bound", ctx.interaction.locale))
            return
        if result == -2:
            await ctx.followup.send(localise("cog.interchat.answers.bind.is_a_hub", ctx.interaction.locale))
            return
        if result == -3:
            await ctx.followup.send(localise("cog.interchat.answers.bind.already_bound", ctx.interaction.locale))
            return

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.interchat.commands.begin.name"),
        description_localizations=localise("cog.interchat.commands.begin.desc"))
    async def begin(self, ctx: discord.ApplicationContext, address: discord.Option(str,
            name_localizations=localise("cog.interchat.commands.begin.options.address.name"),
            description=localise("cog.interchat.commands.begin.options.address.desc", DEFAULT_LOCALE),
            description_localizations=localise("cog.interchat.commands.begin.options.address.desc"),
        )):
        if ctx.author.id in interchat_bans["begin"]:
            await ctx.respond(localise("generic.banned_from_command", ctx.interaction.locale), ephemeral=True)
            return
        addrs = self.db.search(Query().address == address)
        if len(addrs) == 0:
            await ctx.respond(localise("cog.interchat.answers.begin.fail.not_found", ctx.interaction.locale))
            return
        chid = addrs[0]["chid"]
        guid = addrs[0]["guid"]
        channel = self.bot.get_channel(chid) or self.bot.get_partial_messageable(chid)
        if channel == ctx.channel:
            await ctx.respond(localise("cogs.interchat.answers.begin.fail.same_channel", ctx.interaction.locale), ephemeral=True)
            return
        await ctx.response.defer(ephemeral=True)
        if await self.start_interchat(ctx.channel, channel):
            embed = discord.Embed()
            embed.title = localise("cog.interchat.answers.begin.incoming", DEFAULT_LOCALE)
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.started", DEFAULT_LOCALE), value=f"<t:{round(time.time())}:F>")
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.our_side", DEFAULT_LOCALE), value=localise("cog.interchat.answers.info.receiver_side", DEFAULT_LOCALE))
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.incoming_to", DEFAULT_LOCALE), value=self.address_string(channel))
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.outgoing_from", DEFAULT_LOCALE), value=self.address_string(ctx.channel))
            embed.color = discord.Color.green()
            await channel.send(embed=embed)

            embed = discord.Embed()
            embed.title = localise("cog.interchat.answers.begin.outgoing", DEFAULT_LOCALE)
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.started", DEFAULT_LOCALE), value=f"<t:{round(time.time())}:F>")
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.our_side", DEFAULT_LOCALE), value=localise("cog.interchat.answers.info.opener_side", DEFAULT_LOCALE))
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.incoming_to", DEFAULT_LOCALE), value=self.address_string(channel))
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.outgoing_from", DEFAULT_LOCALE), value=self.address_string(ctx.channel))
            embed.color = discord.Color.green()
            await ctx.channel.send(embed=embed)

            await ctx.followup.send("OK", ephemeral=True)
        else:
            await ctx.followup.send(localise("cogs.interchat.answers.begin.fail.already_open", ctx.interaction.locale), ephemeral=True)

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.interchat.commands.unbind.name"),
        description_localizations=localise("cog.interchat.commands.unbind.desc"))
    async def unbind(self, ctx: discord.ApplicationContext, address: discord.Option(str,
            name_localizations=localise("cog.interchat.commands.unbind.options.address.name"),
            description=localise("cog.interchat.commands.unbind.options.address.desc", DEFAULT_LOCALE),
            description_localizations=localise("cog.interchat.commands.unbind.options.address.desc"),
        )):
        if ctx.author.id in interchat_bans["unbind"]:
            await ctx.respond(localise("generic.banned_from_command", ctx.interaction.locale), ephemeral=True)
            return
        await ctx.response.defer(ephemeral=True)
        result = await self.unbind_interchat_hub(address, ctx.channel)
        if result == 1:
            await ctx.followup.send(localise("cog.interchat.answers.unbind.success", ctx.interaction.locale))

            hub = self.get_hub(addr=address)

            embed = discord.Embed()
            embed.title = localise("cog.interchat.answers.unbind.incoming", DEFAULT_LOCALE)
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.started", DEFAULT_LOCALE), value=f"<t:{round(time.time())}:F>")
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.our_side", DEFAULT_LOCALE), value=localise("cog.interchat.answers.info.receiver_side", DEFAULT_LOCALE))
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.hub.incoming_to", DEFAULT_LOCALE), value=self.address_string_hub(self.bot.get_channel(hub["host"])))
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.outgoing_from", DEFAULT_LOCALE), value=self.address_string(ctx.channel))
            embed.color = discord.Color.green()
            await self.bot.get_channel(hub["host"]).send(embed=embed)
            for channel in hub["channels"]:
                await self.bot.get_channel(channel).send(embed=embed)

            embed = discord.Embed()
            embed.title = localise("cog.interchat.answers.unbind.outgoing", DEFAULT_LOCALE)
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.started", DEFAULT_LOCALE), value=f"<t:{round(time.time())}:F>")
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.our_side", DEFAULT_LOCALE), value=localise("cog.interchat.answers.info.opener_side", DEFAULT_LOCALE))
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.hub.incoming_to", DEFAULT_LOCALE), value=self.address_string_hub(self.bot.get_channel(hub["host"])))
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.outgoing_from", DEFAULT_LOCALE), value=self.address_string(ctx.channel))
            embed.color = discord.Color.green()
            await ctx.channel.send(embed=embed)

            return
        if result == -1:
            await ctx.followup.send(localise("cog.interchat.answers.unbind.not_bound", ctx.interaction.locale))
            return
        if result == -2:
            await ctx.followup.send(localise("cog.interchat.answers.unbind.is_a_hub", ctx.interaction.locale))
            return

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.interchat.commands.destroy_hub.name"),
        description_localizations=localise("cog.interchat.commands.destroy_hub.desc"))
    async def destroy_hub(self, ctx: discord.ApplicationContext):
        if ctx.author.id in interchat_bans["destroy_hub"]:
            await ctx.respond(localise("generic.banned_from_command", ctx.interaction.locale), ephemeral=True)
            return
        hub = self.get_hub(channel=ctx.channel, create=False)
        if not hub:
            await ctx.respond(localise("cogs.interchat.answers.destroy_hub.not_found", ctx.interaction.locale), ephemeral=True)
            return
        await ctx.respond("OK", ephemeral=True)
        for channel in hub["channels"]:
            embed = discord.Embed()
            embed.title = localise("cog.interchat.answers.unbind.outgoing", DEFAULT_LOCALE)
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.started", DEFAULT_LOCALE), value=f"<t:{round(time.time())}:F>")
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.our_side", DEFAULT_LOCALE), value=localise("cog.interchat.answers.info.opened_side", DEFAULT_LOCALE))
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.hub.incoming_to", DEFAULT_LOCALE), value=self.address_string_hub(self.bot.get_channel(hub["host"])))
            embed.add_field(inline=False, name=localise("cog.interchat.answers.info.outgoing_from", DEFAULT_LOCALE), value=self.address_string(self.bot.get_channel(channel)))
            embed.color = discord.Color.green()
            await self.bot.get_channel(channel).send(embed=embed)
            await self.unbind_interchat_hub(hub["address"], self.bot.get_channel(channel))
        self.hdb.remove(Query()["address"] == hub["address"])

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.interchat.commands.end.name"),
        description_localizations=localise("cog.interchat.commands.end.desc"))
    async def end(self, ctx: discord.ApplicationContext):
        if ctx.author.id in interchat_bans["end"]:
            await ctx.respond(localise("generic.banned_from_command", ctx.interaction.locale), ephemeral=True)
            return
        for i, tunnel in enumerate(self.tunnels):
            if ctx.channel.id == tunnel["in"].id or ctx.channel.id == tunnel["out"].id:
                if tunnel["permanent"]:
                    await ctx.respond(localise("cogs.interchat.answers.end.fail.permanent_tunnel", ctx.interaction.locale), ephemeral=True)
                    return
                await ctx.respond("OK", ephemeral=True)

                embed = discord.Embed()
                embed.title = localise("cog.interchat.answers.end.incoming", DEFAULT_LOCALE).format(
                        side=(localise("cog.interchat.answers.info.receiver_side", DEFAULT_LOCALE) if ctx.channel.id == tunnel["in"].id else localise("cog.interchat.answers.info.opener_side", DEFAULT_LOCALE))
                    )
                embed.add_field(inline=False, name=localise("cog.interchat.answers.info.started", DEFAULT_LOCALE), value=f"<t:{tunnel['started']}:F>")
                embed.add_field(inline=False, name=localise("cog.interchat.answers.info.our_side", DEFAULT_LOCALE), value=localise("cog.interchat.answers.info.receiver_side", DEFAULT_LOCALE))
                embed.add_field(inline=False, name=localise("cog.interchat.answers.info.incoming_to", DEFAULT_LOCALE), value=self.address_string(tunnel["in"]))
                embed.add_field(inline=False, name=localise("cog.interchat.answers.info.outgoing_from", DEFAULT_LOCALE), value=self.address_string(tunnel["out"]))
                embed.color = discord.Color.red()
                await tunnel["in"].send(embed=embed)

                embed = discord.Embed()
                embed.title = localise("cog.interchat.answers.end.outgoing", DEFAULT_LOCALE).format(
                        side=(localise("cog.interchat.answers.info.opener_side", DEFAULT_LOCALE) if ctx.channel.id == tunnel["out"].id else localise("cog.interchat.answers.info.receiver_side", DEFAULT_LOCALE))
                    )
                embed.add_field(inline=False, name=localise("cog.interchat.answers.info.started", DEFAULT_LOCALE), value=f"<t:{tunnel['started']}:F>")
                embed.add_field(inline=False, name=localise("cog.interchat.answers.info.our_side", DEFAULT_LOCALE), value=localise("cog.interchat.answers.info.opener_side", DEFAULT_LOCALE))
                embed.add_field(inline=False, name=localise("cog.interchat.answers.info.incoming_to", DEFAULT_LOCALE), value=self.address_string(tunnel["in"]))
                embed.add_field(inline=False, name=localise("cog.interchat.answers.info.outgoing_from", DEFAULT_LOCALE), value=self.address_string(tunnel["out"]))
                embed.color = discord.Color.red()
                await tunnel["out"].send(embed=embed)

                await self.end_interchat(tunnel)
                return

        await ctx.respond(localise("cogs.interchat.answers.end.fail.not_opened", ctx.interaction.locale), ephemeral=True)


    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.interchat.commands.address.name"),
        description_localizations=localise("cog.interchat.commands.address.desc"))
    async def address(self, ctx: discord.ApplicationContext):
        if ctx.author.id in interchat_bans["address"]:
            await ctx.respond(localise("generic.banned_from_command", ctx.interaction.locale), ephemeral=True)
            return
        await ctx.respond(localise("cog.interchat.answers.getaddress", ctx.interaction.locale).format(address=self.get_address(ctx.channel)))

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.interchat.commands.info.name"),
        description_localizations=localise("cog.interchat.commands.info.desc"))
    async def info(self, ctx: discord.ApplicationContext):
        if ctx.author.id in interchat_bans["info"]:
            await ctx.respond(localise("generic.banned_from_command", ctx.interaction.locale), ephemeral=True)
            return

        this_tunnel = None
        for i, tunnel in enumerate(self.tunnels):
            if ctx.channel == tunnel["in"] or ctx.channel == tunnel["out"]:
                this_tunnel = tunnel
                break
        embed = discord.Embed(title=localise("cog.interchat.answers.info.title", ctx.interaction.locale))
        if not this_tunnel:
            embed.description = localise("cog.interchat.answers.info.offline", ctx.interaction.locale)
            embed.color = discord.Color.red()
            await ctx.respond(embed=embed)
            return
        embed.description = localise("cog.interchat.answers.info.online", ctx.interaction.locale)
        embed.add_field(inline=False, name=localise("cog.interchat.answers.info.started", ctx.interaction.locale), value=f"<t:{this_tunnel['started']}:F>")
        embed.add_field(inline=False, name=localise("cog.interchat.answers.info.our_side", ctx.interaction.locale), value=(localise("cog.interchat.answers.info.receiver_side", ctx.interaction.locale) if ctx.channel.id == this_tunnel["in"].id else localise("cog.interchat.answers.info.opener_side", ctx.interaction.locale)))
        embed.add_field(inline=False, name=localise("cog.interchat.answers.info.incoming_to", ctx.interaction.locale), value=self.address_string(this_tunnel["in"]))
        embed.add_field(inline=False, name=localise("cog.interchat.answers.info.outgoing_from", ctx.interaction.locale), value=self.address_string(this_tunnel["out"]))
        embed.add_field(inline=False, name=localise("cog.interchat.answers.info.permanent", ctx.interaction.locale), value=(localise("generic.yes", ctx.interaction.locale) if this_tunnel["permanent"] else localise("generic.no", ctx.interaction.locale)))
        embed.color = discord.Color.blurple()
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(interchat(bot))

def teardown(bot):
    bot.loop.call_soon(bot.get_cog("interchat").unload)
