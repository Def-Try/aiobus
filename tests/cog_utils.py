import asyncio

from .core import Bot
from .core import Context
from .core import discordtest as test
from .core import User
from cogs import util as _cog


@test("GTFU w/ no asker")
def test1():
    bot = Bot()
    _cog.setup(bot)
    assert len(bot.cogs) == 1
    cog = bot.cogs[list(bot.cogs.items())[0][0]]
    assert cog != None

    async def runner():
        ctx = Context()
        await cog.googleforyou(cog, ctx, "test")
        assert (
            ctx.content
            == "Let me google that for you...\n[here!](<https://googlethatforyou.com/?q=test>)"
        )

    # setting up asyncio loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runner())


@test("GTFU w/ asker")
def test2():
    bot = Bot()
    _cog.setup(bot)
    assert len(bot.cogs) == 1
    cog = bot.cogs[list(bot.cogs.items())[0][0]]
    assert cog != None

    async def runner():
        ctx = Context()
        await cog.googleforyou(cog, ctx, "test", User())
        assert (
            ctx.content
            == "Let me google that for you, <@1234567890>...\n[here!](<https://googlethatforyou.com/?q=test>)"
        )

    # setting up asyncio loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runner())


tests = [test1, test2]
