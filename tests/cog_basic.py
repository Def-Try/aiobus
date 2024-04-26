import asyncio

from .core import Bot
from .core import Context
from .core import discordtest as test
from .core import User
from cogs import basic as _cog

bot = Bot()
cog = None

@test("basic cog pre init")
def test1():
    global cog
    _cog.setup(bot)
    assert len(bot.cogs) == 1
    cog = bot.cogs[list(bot.cogs.items())[0][0]]
    assert cog != None
    for cmd in cog.get_commands():
         cmd.cog = cog


@test("basic cog complete init")
def test2():
    global cog
    assert cog != None

    async def runner():
        await cog.complete_init()

    # setting up asyncio loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runner())


@test("help command")
def test3():
    global cog
    assert cog != None

    async def runner():
        ctx = Context()
        await cog.help(ctx)
        assert ctx.ephemeral == True
        assert len(ctx.embeds) > 0
        ctx = Context()
        await cog.help(ctx, command="ping")
        assert ctx.ephemeral == True
        assert len(ctx.embeds) > 0
        ctx = Context()
        await cog.help(ctx, cog="basic")
        assert ctx.ephemeral == True
        assert len(ctx.embeds) > 0

    # setting up asyncio loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runner())

tests = [test1, test2, test3]
