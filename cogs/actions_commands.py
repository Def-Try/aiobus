import discord
from discord.ext import commands
from nekosbest import Client, Result
import json
from localisation import LOCALISATIONS

with open("config.cfg", 'r') as f:
    CONFIG = json.loads(f.read())

nekosbest_client = Client()

portals_awaiting = {}

class actions_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    acts_1 = discord.SlashCommandGroup("actions_1", "",
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["command_group"]["name"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["command_group"]["desc"])
    acts_2 = discord.SlashCommandGroup("actions_2", "",
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["command_group"]["name"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["command_group"]["desc"])

    # регион ПЕРВАЯ ГРУППА
    #  регион ОБЫЧНЫЕ ДЕЙСТВИЯ

    async def act(self, action: str, ctx: discord.ApplicationContext):
        result = await nekosbest_client.get_image(action, 1)
        locale = ctx.interaction.locale
        localis_act = LOCALISATIONS["cog"]["actions_commands"]["answers"]["action"][action]
        embed = discord.Embed(
            title=LOCALISATIONS["cog"]["actions_commands"]["answers"]["action"]["name"].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}"),
            description=localis_act['self'].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}").replace("{member}", ctx.author.mention),
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    async def act_req_other(self, action: str, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        result = await nekosbest_client.get_image(action, 1)
        locale = ctx.interaction.locale
        localis_act = LOCALISATIONS["cog"]["actions_commands"]["answers"]["action"][action]
        embed = discord.Embed(
            title=LOCALISATIONS["cog"]["actions_commands"]["answers"]["action"]["name"].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}"),
            description=localis_act['self'].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}").replace("{member}", ctx.author.mention) 
                    if other == ctx.author else 
                localis_act['bot'].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}").replace("{member}", ctx.author.mention) 
                    if other == self.bot.user else
                localis_act["other"].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}").replace("{member}", ctx.author.mention).replace("{other}", other.mention),
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    async def act_with_other(self, action: str, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)=None):
        result = await nekosbest_client.get_image(action, 1)
        locale = ctx.interaction.locale
        localis_act = LOCALISATIONS["cog"]["actions_commands"]["answers"]["action"][action]
        embed = discord.Embed(
            title=LOCALISATIONS["cog"]["actions_commands"]["answers"]["action"]["name"].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}"),
            description=localis_act['self'].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}").replace("{member}", ctx.author.mention) 
                    if other == ctx.author else 
                localis_act['bot'].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}").replace("{member}", ctx.author.mention) 
                    if other == self.bot.user else
                localis_act["other"].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}").replace("{member}", ctx.author.mention).replace("{other}", other.mention)
                    if other else
                localis_act["none"].get(locale, f"ERR: LOCALE_NOT_FOUND: {locale}").replace("{member}", ctx.author.mention),
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["pat"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def pat(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        await self.act_req_other("pat", ctx, other)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["hug"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def hug(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        await self.act_req_other("hug", ctx, other)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["cuddle"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def cuddle(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        await self.act_req_other("cuddle", ctx, other)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["handshake"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def handshake(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        await self.act_req_other("handshake", ctx, other)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["bite"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def bite(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        await self.act_req_other("bite", ctx, other)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["highfive"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def highfive(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        await self.act_req_other("highfive", ctx, other)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["kiss"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def kiss(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        await self.act_req_other("kiss", ctx, other)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["poke"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def poke(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        await self.act_req_other("poke", ctx, other)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["slap"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def slap(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        await self.act_req_other("slap", ctx, other)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["handhold"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def handhold(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        await self.act_req_other("handhold", ctx, other)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["kick"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def kick(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        await self.act_req_other("kick", ctx, other)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["punch"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def punch(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        await self.act_req_other("punch", ctx, other)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["tickle"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def tickle(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        await self.act_req_other("tickle", ctx, other)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["feed"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def feed(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        await self.act_req_other("feed", ctx, other)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["stare"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def stare(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)=None):
        await self.act_with_other("stare", ctx, other)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["wave"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def wave(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)=None):
        await self.act_with_other("wave", ctx, other)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["cry"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def cry(self, ctx: discord.ApplicationContext):
        await self.act("cry", ctx)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["dance"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def dance(self, ctx: discord.ApplicationContext):
        await self.act("dance", ctx)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["blush"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def blush(self, ctx: discord.ApplicationContext):
        await self.act("blush", ctx)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["happy"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def happy(self, ctx: discord.ApplicationContext):
        await self.act("happy", ctx)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["laugh"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def laugh(self, ctx: discord.ApplicationContext):
        await self.act("laugh", ctx)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["shrug"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def shrug(self, ctx: discord.ApplicationContext):
        await self.act("shrug", ctx)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["sleep"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def sleep(self, ctx: discord.ApplicationContext):
        await self.act("sleep", ctx)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["smile"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def smile(self, ctx: discord.ApplicationContext):
        await self.act("smile", ctx)

    @acts_1.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["think"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def think(self, ctx: discord.ApplicationContext):
        await self.act("think", ctx)

    #  конец региона ОБЫЧНЫЕ ДЕЙСТВИЯ
    # конец региона ПЕРВАЯ ГРУППА

    # регион ВТОРАЯ ГРУППА
    #  регион ОБЫЧНЫЕ ДЕЙСТВИЯ

    @acts_2.command(guild_ids=CONFIG["g_ids"],
        name_localizations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["nod"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["action"]["desc"])
    async def nod(self, ctx: discord.ApplicationContext):
        await self.act("nod", ctx)

    #  конец региона ОБЫЧНЫЕ ДЕЙСТВИЯ
    #  регион ИНТЕРАКТИВНЫЕ ДЕЙСТВИЯ

    @acts_2.command(guild_ids=CONFIG["g_ids"],
        name_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["portal"]["name"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["portal"]["desc"])
    async def portal(self, ctx: discord.ApplicationContext):
        if ctx.author.id in portals_awaiting.keys():

            embed = discord.Embed(
                title="Открытие портала",
                description=f"{ctx.author.mention} открывает портал в {ctx.channel.mention}!",
                color=discord.Colour.blurple(),
            )
            await portals_awaiting[ctx.author.id].send(embed=embed)
            embed = discord.Embed(
                title="Открытие портала",
                description=f"Сюда открывается портал из {portals_awaiting[ctx.author.id].channel.mention}!",
                color=discord.Colour.blurple(),
            )
            await ctx.send(embed=embed)

            del portals_awaiting[ctx.author.id]
            await ctx.respond("Готово! Портал открыт.", ephemeral=True)
            return
        portals_awaiting[ctx.author.id] = ctx
        await ctx.respond("Отлично! Теперь напишите эту же команду в канале, куда вы хотите открыть портал.", ephemeral=True)

    @acts_2.command(guild_ids=CONFIG["g_ids"],
        name_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["portal_cancel"]["name"],
        description_localisations=LOCALISATIONS["cog"]["actions_commands"]["commands"]["portal_cancel"]["desc"])
    async def portal_cancel(self, ctx: discord.ApplicationContext):
        del portals_awaiting[ctx.author.id]
        await ctx.respond("Открытие портала отменено.", ephemeral=True)

    #  конец региона ИНТЕРАКТИВНЫЕ ДЕЙСТВИЯ
    # конец региона ВТОРАЯ ГРУППА

def setup(bot):
    bot.add_cog(actions_commands(bot))
