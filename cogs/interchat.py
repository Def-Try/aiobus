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

class interchat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = TinyDB('databases/interchat.db')
        self.tdb = TinyDB('databases/interchat_tunnels.db')
        self.tunnels = []

    @commands.Cog.listener("on_ready")
    async def complete_init_interchat(self):
        for tunnel in self.tdb:
            self.tunnels.append({})
            rtunnel = self.tunnels[-1]
            rtunnel["out"] = self.bot.get_guild(tunnel["outguid"]).get_channel(tunnel["out"])
            rtunnel["in"] = self.bot.get_guild(tunnel["inguid"]).get_channel(tunnel["in"])
            rtunnel["outwhook"] = await discord.Webhook.from_url(tunnel["outwhook"], session=aiohttp.ClientSession()).fetch()
            rtunnel["inwhook"] = await discord.Webhook.from_url(tunnel["inwhook"], session=aiohttp.ClientSession()).fetch()
            rtunnel["messages"] = list(filter(lambda x: x, [await rtunnel["out" if i[1] else "in"].fetch_message(i[0]) for i in tunnel["messages"]]))
            rtunnel["rmessages"] = list(filter(lambda x: x, [await rtunnel["out" if i[1] else "in"].fetch_message(i[0]) for i in tunnel["rmessages"]]))
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
            self.db.insert({"chid": channel.id, "address": addr, "guid": channel.guild.id})
        return addr

    def generate_address(self):
        c = (string.ascii_uppercase + string.digits)
        return "".join(random.choices(c, k=3))+"-"+"".join(random.choices(c, k=4))+"-"+"".join(random.choices(c, k=2))

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
        self.tunnels.append({"out": fromch, "in": toch, 
            "messages": [], "rmessages": [], "permanent": False,
            "outwhook": await fromch.create_webhook(name="Outgoing interserver tunnel"),
            "inwhook":  await toch.create_webhook(name="Incoming interserver tunnel"),
            "started": round(time.time())})
        self.tdb.insert({"in": toch.id, "out": fromch.id, 'inguid': toch.guild.id, 'outguid': fromch.guild.id,
            "messages": [], "rmessages": [], "permanent": False,
            "inwhook": self.tunnels[-1]["inwhook"].url, "outwhook": self.tunnels[-1]["outwhook"].url,
            "started": round(time.time())})
        return True

    async def end_interserver(self, tunnel):
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
        if message.author.id == self.bot.user.id: return
        for itunnel in self.tunnels:
            if message.author.id == itunnel["outwhook"].id or message.author.id == itunnel["inwhook"].id: return
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
                itunnel["messages"].append(
                    await itunnel["inwhook"].send(message.content, 
                        username=(message.author.name if isinstance(message.author, discord.User) or not message.author.nick else message.author.nick),
                        avatar_url=(message.author.default_avatar.url if not message.author.avatar.url else message.author.avatar.url),
                        embeds=(message.embeds or []) + sticker_embeds + ([ref_embed] if ref_embed else []),
                        files=[await i.to_file() for i in message.attachments],
                        wait=True
                        )
                    )
                itunnel["rmessages"].append(message)
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
                itunnel["messages"].append(
                    await itunnel["outwhook"].send(message.content, 
                        username=(message.author.name if isinstance(message.author, discord.User) or not message.author.nick else message.author.nick),
                        avatar_url=(message.author.default_avatar.url if not message.author.avatar.url else message.author.avatar.url),
                        embeds=(message.embeds or []) + sticker_embeds + ([ref_embed] if ref_embed else []),
                        files=[await i.to_file() for i in message.attachments],
                        wait=True
                        )
                    )
                itunnel["rmessages"].append(message)
                await self.update_interserver(itunnel)
                break

    @commands.Cog.listener("on_message_edit")
    async def tunneling_onmsgedit(self, message_before, message):
        if message.author.id == self.bot.user.id: return
        for itunnel in self.tunnels:
            if message.author.id == itunnel["outwhook"].id or message.author.id == itunnel["inwhook"].id: return
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
                itunnel["messages"][itunnel["rmessages"].index(message_before)] = await itunnel["inwhook"].edit_message(itunnel["messages"][itunnel["rmessages"].index(message_before)].id,
                        content=message.content, 
                        embeds=(message.embeds or []) + sticker_embeds + ([ref_embed] if ref_embed else []),
                        files=[await i.to_file() for i in message.attachments]
                    )
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
                itunnel["messages"][itunnel["rmessages"].index(message_before)] = await itunnel["outwhook"].edit_message(itunnel["messages"][itunnel["rmessages"].index(message_before)].id,
                        content=message.content, 
                        embeds=(message.embeds or []) + sticker_embeds + ([ref_embed] if ref_embed else []),
                        files=[await i.to_file() for i in message.attachments]
                    )
                itunnel["rmessages"][itunnel["rmessages"].index(message_before)] = message
                await self.update_interserver(itunnel)
                break

    @commands.Cog.listener("on_message_delete")
    async def tunneling_onmsgdel(self, message):
        if message.author.id == self.bot.user.id: return
        for itunnel in self.tunnels:
            if message.author.id == itunnel["outwhook"].id or message.author.id == itunnel["inwhook"].id: return
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
        addrs = self.db.search(Query().address == address)
        if len(addrs) == 0:
            await ctx.respond(localise("cog.interchat.answers.begin.notfound"))
            return
        chid = addrs[0]["chid"]
        guid = addrs[0]["guid"]
        guild = self.bot.get_guild(guid)
        channel = guild.get_channel(chid)
        if channel == ctx.channel:
            await ctx.respond("Unable to open interchat tunnel to the same channel you are in.", ephemeral=True)
        await ctx.response.defer(ephemeral=True)
        if await self.start_interserver(ctx.channel, channel):
            await channel.send(f"# Incoming interchat communication channel.\nTunnel opened - `{self.get_address(ctx.channel)}` requested connection.\n{ctx.channel.guild.name if not isinstance(ctx.channel, discord.abc.PrivateChannel) else 'DM'} - {ctx.channel.name if not isinstance(ctx.channel, discord.abc.PrivateChannel) else ctx.channel.recipient.name}")
            await ctx.channel.send(f"# Outgoing interchat communication channel.\nTunnel opened - `{self.get_address(channel)}` requested connection.\n{channel.guild.name if not isinstance(channel, discord.abc.PrivateChannel) else 'DM'} - {channel.name if not isinstance(channel, discord.abc.PrivateChannel) else channel.recipient.name}")
            await ctx.followup.send("OK", ephemeral=True)
        else:
            await ctx.followup.send("Tunnel failed to open - there is already online connection using that address.", ephemeral=True)

    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.interchat.commands.end.name"),
        description_localisations=localise("cog.interchat.commands.end.desc"))
    async def end(self, ctx: discord.ApplicationContext):
        for i, tunnel in enumerate(self.tunnels):
            if ctx.channel == tunnel["in"]:
                if tunnel["permanent"]:
                    await ctx.respond("Unable to close permanent tunnel. Contact googer_ if you want to move or close this tunnel.")
                    return
                await ctx.respond("OK", ephemeral=True)
                await ctx.channel.send("# Incoming interchat communication channel ended by this side.\nTunnel closed.")
                await tunnel["out"].send("# Outgoing interchat communication channel ended by receiver side.\nTunnel closed.")
                await self.end_interserver(tunnel)
                self.tunnels.pop(i)
                return
            if ctx.channel == tunnel["out"]:
                if tunnel["permanent"]:
                    await ctx.respond("Unable to close permanent tunnel. Contact googer_ if you want to move or close this tunnel.")
                    return
                await ctx.respond("OK", ephemeral=True)
                await ctx.channel.send("# Outgoing interchat communication channel ended by this side.\nTunnel closed.")
                await tunnel["in"].send("# Incoming interchat communication channel ended by opener side.\nTunnel closed.")
                await self.end_interserver(tunnel)
                self.tunnels.pop(i)
                return
        await ctx.respond("No opened tunnel for this channel has been found", ephemeral=True)



    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.interchat.commands.address.name"),
        description_localisations=("cog.interchat.commands.address.desc"))
    async def address(self, ctx: discord.ApplicationContext):
        await ctx.respond(localise("cog.interchat.answers.getaddress", ctx.interaction.locale).format(address=self.get_address(ctx.channel)))
        
    @cmds.command(guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.interchat.commands.info.name"),
        description_localisations=("cog.interchat.commands.info.desc"))
    async def info(self, ctx: discord.ApplicationContext):
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
            channel_out=f"{tunnel[out].guild.name if not isinstance(tunnel['out'], discord.abc.PrivateChannel) else 'DM'}, {tunnel['out'].name if not isinstance(tunnel['out'], discord.abc.PrivateChannel) else tunnel['out'].recipient.name}",
            address_out=self.get_address(tunnel["out"]),
            out_here=("(here)" if ctx.channel == tunnel["out"] else ""),
            channel_in=f"{tunnel['in'].guild.name if not isinstance(tunnel['in'], discord.abc.PrivateChannel) else 'DM'}, {tunnel['in'].name if not isinstance(tunnel['in'], discord.abc.PrivateChannel) else tunnel['in'].recipient.name}",
            address_in=self.get_address(tunnel["in"]),
            in_here=("(here)" if ctx.channel == tunnel["in"] else ""),
            permanent=("Yes" if tunnel["permanent"] else "No")
        ))
        

def setup(bot):
    bot.add_cog(interchat(bot))
