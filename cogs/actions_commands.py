import discord
from discord.ext import commands

from nekosbest import Client, Result

import json
with open("config.cfg", 'r') as f:
    CONFIG = json.loads(f.read())

nekosbest_client = Client()

portals_awaiting = {}

class actions_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    acts_1 = discord.SlashCommandGroup("действие_1", "РП и не очень действия. Первая группа, из-за ограничений дискорда")
    acts_2 = discord.SlashCommandGroup("действие_2", "РП и не очень действия. Вторая группа, из-за ограничений дискорда")

    def parse_action_answer(self, ctx, other):
        return 'сам себя' if other == ctx.author else str(other.mention) if other != self.bot.user else 'меня'

    def parse_action_answer_of(self, ctx, other):
        return 'себе '+item if other == ctx.author else item+" "+str(other.mention) if other != self.bot.user else 'мою '+item

    def parse_action_answer_to(self, ctx, other):
        return 'к себе... как?' if other == ctx.author else "к "+str(other.mention) if other != self.bot.user else 'ко мне'

    # регион ПЕРВАЯ ГРУППА
    #  регион ОБЫЧНЫЕ ДЕЙСТВИЯ

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="погладить", description="Погладить другого пользователя.")
    async def pat(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        result = await nekosbest_client.get_image("pat", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} гладит {self.parse_action_answer(ctx, other)}!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="обнять", description="Обнять другого пользователя.")
    async def hug(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        result = await nekosbest_client.get_image("hug", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} обнимает {self.parse_action_answer(ctx, other)}!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="прижаться", description="Прижаться к другому пользователю.")
    async def cuddle(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        result = await nekosbest_client.get_image("cuddle", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} прижимается {self.parse_action_answer_to(ctx, other)}!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="пожать_руку", description="Пожать руку другому пользователю.")
    async def handshake(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        result = await nekosbest_client.get_image("handshake", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} пожимает {self.parse_action_answer_of(ctx, other, 'руку')}!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="укусить", description="Укусить другого пользователя.")
    async def bite(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        result = await nekosbest_client.get_image("bite", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} кусает {self.parse_action_answer(ctx, other)}!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="дать_пять", description="Дать пять другому пользователю.")
    async def highfive(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        result = await nekosbest_client.get_image("highfive", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} даёт пять {'себе' if other == ctx.author else str(other.mention) if other != self.bot.user else 'мне'}!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="поцеловать", description="Поцеловать другого пользователя.")
    async def kiss(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        result = await nekosbest_client.get_image("kiss", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} целует {self.parse_action_answer(ctx, other)}!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="тыкать", description="Тыкать в другого пользователя.")
    async def slap(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        result = await nekosbest_client.get_image("slap", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} тыкает в {'самого себя' if other == ctx.author else str(other.mention) if other != self.bot.user else 'меня'}!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="шлепнуть", description="Шлёпнуть другого пользователя.")
    async def slap(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        result = await nekosbest_client.get_image("slap", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} шлёпает {self.parse_action_answer(ctx, other)}!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="держать_за_руку", description="Взять другого пользователя за руку.")
    async def handhold(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        result = await nekosbest_client.get_image("handhold", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} держится за руки с {'самим собой' if other == ctx.author else str(other.mention) if other != self.bot.user else 'ботом'}!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="пнуть", description="Пнуть другого пользователя.")
    async def kick(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        result = await nekosbest_client.get_image("kick", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} пинает {self.parse_action_answer(ctx, other)}!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="ударить", description="Ударить другого пользователя.")
    async def punch(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        result = await nekosbest_client.get_image("punch", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} ударяет {self.parse_action_answer(ctx, other)}!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="щекотать", description="Пощекотать другого пользователя.")
    async def tickle(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        result = await nekosbest_client.get_image("tickle", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} щекочет {self.parse_action_answer(ctx, other)}!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="кормить", description="Покормить другого пользователя.")
    async def feed(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)):
        result = await nekosbest_client.get_image("feed", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} кормит {self.parse_action_answer(ctx, other)}!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="смотреть", description="Смотреть на что-то или на другого пользователя.")
    async def stare(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)=None):
        result = await nekosbest_client.get_image("stare", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} смотрит на {'что-то' if other is None else self.parse_action_answer(ctx, other)}!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="махать_рукой", description="Махать рукой просто так или другому пользователю.")
    async def wave(self, ctx: discord.ApplicationContext, other: discord.Option(discord.Member)=None):
        result = await nekosbest_client.get_image("wave", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} машет рукой{'' if other is None else ' '+self.parse_action_answer(ctx, other)}!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="плакать", description="Плакать.")
    async def cry(self, ctx: discord.ApplicationContext):
        result = await nekosbest_client.get_image("cry", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} плачет!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="покраснеть", description="Покраснеть.")
    async def blush(self, ctx: discord.ApplicationContext):
        result = await nekosbest_client.get_image("blush", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} краснеет!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="танец", description="Танцевать.")
    async def dance(self, ctx: discord.ApplicationContext):
        result = await nekosbest_client.get_image("dance", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} танцует!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="радоваться", description="Радоваться.")
    async def happy(self, ctx: discord.ApplicationContext):
        result = await nekosbest_client.get_image("happy", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} радуется!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="смеяться", description="Смеяться.")
    async def laugh(self, ctx: discord.ApplicationContext):
        result = await nekosbest_client.get_image("laugh", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} смеётся!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="пожать_плечами", description="Пожать плечами.")
    async def shrug(self, ctx: discord.ApplicationContext):
        result = await nekosbest_client.get_image("shrug", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} пожимает плечами!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="спать", description="Спать.")
    async def sleep(self, ctx: discord.ApplicationContext):
        result = await nekosbest_client.get_image("sleep", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} спит!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="улыбнуться", description="Улыбнуться.")
    async def smile(self, ctx: discord.ApplicationContext):
        result = await nekosbest_client.get_image("smile", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} улыбается!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    @acts_1.command(guild_ids=CONFIG["g_ids"], name="думать", description="Думать.")
    async def think(self, ctx: discord.ApplicationContext):
        result = await nekosbest_client.get_image("think", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} думает!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    #  конец региона ОБЫЧНЫЕ ДЕЙСТВИЯ
    # конец региона ПЕРВАЯ ГРУППА

    # регион ВТОРАЯ ГРУППА
    #  регион ОБЫЧНЫЕ ДЕЙСТВИЯ

    @acts_2.command(guild_ids=CONFIG["g_ids"], name="кивнуть", description="Кивнуть.")
    async def nod(self, ctx: discord.ApplicationContext):
        result = await nekosbest_client.get_image("nod", 1)
        embed = discord.Embed(
            title="Действие",
            description=f"{ctx.author.mention} кивает!",
            color=discord.Colour.blurple(),
        )
        embed.set_image(url=result.url)
        await ctx.respond(embed=embed)

    #  конец региона ОБЫЧНЫЕ ДЕЙСТВИЯ
    #  регион ИНТЕРАКТИВНЫЕ ДЕЙСТВИЯ

    @acts_2.command(guild_ids=CONFIG["g_ids"], name="открыть_портал", description="Начать открытие портала.")
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
    @acts_2.command(guild_ids=CONFIG["g_ids"], name="отменить_портал", description="Отменить открытие портала.")
    async def portal_cancel(self, ctx: discord.ApplicationContext):
        del portals_awaiting[ctx.author.id]
        await ctx.respond("Открытие портала отменено.", ephemeral=True)

    #  конец региона ИНТЕРАКТИВНЫЕ ДЕЙСТВИЯ
    # конец региона ВТОРАЯ ГРУППА

def setup(bot):
    bot.add_cog(actions_commands(bot))
