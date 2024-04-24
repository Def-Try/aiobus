import asyncio

from .core import add_tests
from .core import Bot
from .core import Context
from .core import discordtest as test
from .core import importfile
from .core import run as run_tests
from cogs import util as _cog


@test("GTFU w/ no asker")
def test1():
    bot = Bot()
    _cog.setup(bot)
    assert len(bot.cogs) == 1
    cog = bot.cogs[0]
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


add_tests([test1])

run_tests()
