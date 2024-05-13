import json
import time
import io
import datetime

import aiohttp
import discord
from discord.ext import commands
from openai import AsyncOpenAI
from tinydb import Query
from tinydb import TinyDB

from config import CONFIG
from config import TOKENS
from localisation import DEFAULT_LOCALE
from localisation import localise
from utilities import download_file


class AICog(commands.Cog, name="ai"):
    author = "googer_"

    def __init__(self, bot):
        self.bot = bot

        self.db = TinyDB("databases/ai.db")

        self.udata = {}

        self.cooldowns = {}

        for udata in self.db:
            self.udata[udata["key"]] = udata["data"]

        self.openai = AsyncOpenAI(
            api_key=TOKENS["deepinfra"],
            base_url="https://api.deepinfra.com/v1/openai",
        )

        self.template = """
You are a googer AI. The first sentient AI in the world.
The current time and date is: {}
Try to be a helpful assistant. Conform your users requests.
""".strip()

    def get_udata_id(self, anchor):
        if hasattr(anchor, "guild"):
            return anchor.guild.id
        return anchor.channel.id

    def get_udata(self, udataid):
        return self.udata.get(
            str(udataid),
            {
                "ai": [
                    [{"role": "system", "content": self.template}],
                ],
                "settings": {"allowmode": "blacklist", "list": []},
            },
        )

    cmds = discord.SlashCommandGroup(
        "ai",
        "",
        name_localizations=localise("cog.ai.command_group.name"),
        description_localizations=localise("cog.ai.command_group.desc"),
    )

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.ai.commands.draw.name"),
        description_localizations=localise("cog.ai.commands.draw.desc"),
    )
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def draw(
        self,
        ctx: discord.ApplicationContext,
        prompt: discord.Option(
            str,
            name_localizations=localise("cog.ai.commands.draw.options.prompt.name"),
            description=localise(
                "cog.ai.commands.draw.options.prompt.desc", DEFAULT_LOCALE
            ),
            description_localizations=localise(
                "cog.ai.commands.draw.options.prompt.desc"
            ),
        ),
    ):
        await ctx.response.defer()

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url="https://fal.run/fal-ai/fast-lightning-sdxl",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Key {TOKENS['fal']}",
                },
                data=json.dumps({"prompt": prompt, "enable_safety_checker": True}),
            )
            response = await response.json()

        if (
            isinstance(ctx.channel, discord.Thread) and ctx.channel.parent.nsfw
        ) or ctx.channel.nsfw or not any(response["has_nsfw_concepts"]):
            async with aiohttp.ClientSession() as session:
                status = await download_file(session, response["images"][0]["url"])
                if status["error"]:
                    await ctx.followup.send(status["error"])
                    return
                with io.BytesIO(status["data"]) as fp:
                    await ctx.followup.send(file=discord.File(fp, "generated.jpeg"))
            return
        await ctx.followup.send(
            localise("cog.ai.answers.draw.nsfw_detected", ctx.interaction.locale)
        )

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.ai.commands.rollback.name"),
        description_localizations=localise("cog.ai.commands.rollback.desc"),
    )
    @commands.has_guild_permissions(manage_messages=True)
    @commands.guild_only()
    async def rollback(
        self,
        ctx: discord.ApplicationContext,
    ):
        udata = self.get_udata(self.get_udata_id(ctx))
        self.udata[self.get_udata_id(ctx)] = udata

        if len(udata["ai"][0]) > 1:
            udata["ai"][0] = udata["ai"][0][:-2]

        self.db.upsert(
            {
                "key": str(self.get_udata_id(ctx)),
                "data": self.udata[self.get_udata_id(ctx)],
            },
            Query().key == self.get_udata_id(ctx),
        )

        await ctx.respond(
            localise("cog.ai.answers.context.rollback", ctx.interaction.locale)
        )

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.ai.commands.reset_messages.name"),
        description_localizations=localise("cog.ai.commands.reset_messages.desc"),
    )
    @commands.has_guild_permissions(manage_messages=True)
    @commands.guild_only()
    async def reset_messages(self, ctx: discord.ApplicationContext):
        udata = self.get_udata(self.get_udata_id(ctx))
        self.udata[self.get_udata_id(ctx)] = udata

        udata["ai"][0] = [{"role": "system", "content": self.template}]

        self.db.upsert(
            {
                "key": str(self.get_udata_id(ctx)),
                "data": self.udata[self.get_udata_id(ctx)],
            },
            Query().key == self.get_udata_id(ctx),
        )

        await ctx.respond(
            localise("cog.ai.answers.reset.messages", ctx.interaction.locale)
        )

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.ai.commands.context.name"),
        description_localizations=localise("cog.ai.commands.context.desc"),
    )
    async def context(self, ctx: discord.ApplicationContext):
        udata = self.get_udata(self.get_udata_id(ctx))
        self.udata[self.get_udata_id(ctx)] = udata

        messages = udata["ai"][0][-6:]
        skipped = len(messages) - 6
        if skipped <= 0:
            messages = messages[1:]
            skipped = 0
        if messages == []:
            await ctx.respond(
                localise("cog.ai.answers.context.empty", ctx.interaction.locale)
            )
            return
        # pylint: disable=consider-using-generator
        while sum([len(v["content"]) + len(v["role"]) for v in messages]) > 2000 - 100:
            messages = messages[:-1]
            skipped += 1
        # pylint: enable=consider-using-generator
        if messages == []:
            await ctx.respond(
                localise("cog.ai.answers.context.too_long", ctx.interaction.locale)
            )
            return

        self.db.upsert(
            {
                "key": str(self.get_udata_id(ctx)),
                "data": self.udata[self.get_udata_id(ctx)],
            },
            Query().key == self.get_udata_id(ctx),
        )

        msgctx = ""
        for message in messages:
            if message["role"] == "assistant":
                msgctx += "googerai: "
            msgctx += message["content"] + "\n"
        msgctx = msgctx.strip()

        await ctx.respond(
            localise("cog.ai.answers.context.context", ctx.interaction.locale).format(
                context=msgctx, skipped=skipped
            )
        )

    @cmds.command(
        guild_ids=CONFIG["g_ids"],
        name_localizations=localise("cog.ai.commands.lawsets.name"),
        description_localizations=localise("cog.ai.commands.lawsets.desc"),
    )
    async def lawsets(self, ctx: discord.ApplicationContext):
        lawsets = "* " + "\n* ".join(self.ai_lawsets.keys())
        await ctx.respond(
            localise(
                "cog.ai.answers.change_laws.lawsets", ctx.interaction.locale
            ).format(lawsets=lawsets)
        )

    @commands.Cog.listener("on_message")
    async def talk_onmsg(self, message):
        if self.bot.user not in message.mentions or message.author == self.bot.user:
            return

        if self.cooldowns.get(message.guild.id, 0) > time.time():
            await message.add_reaction("🐢")
            await message.reply(
                localise("generic.error.cooldown", DEFAULT_LOCALE).format(
                    retry_after=round(
                        self.cooldowns.get(message.guild.id, 0) - time.time()
                    )
                ),
                delete_after=10,
            )
            return

        udata = self.get_udata(self.get_udata_id(message))
        self.udata[self.get_udata_id(message)] = udata

        if (
            udata["settings"]["allowmode"] == "whitelist"
            and message.channel.id not in udata["settings"]["list"]
        ):
            return
        if (
            udata["settings"]["allowmode"] == "blacklist"
            and message.channel.id in udata["settings"]["list"]
        ):
            return

        self.cooldowns[message.guild.id] = 2**31 - 1

        messages = udata["ai"][0]
        messages.append(
            {
                "role": "user",
                "content": message.author.name + ": " + message.clean_content,
            }
        )
        smessages = list(messages)
        smessages[0]["content"] = smessages[0]["content"].format(datetime.datetime.now().strftime("%d.%m.%Y %H:%M"))
        async with message.channel.typing():
            result = "Something went terribly wrong."
            fail = False
            try:
                chat_completion = await self.openai.chat.completions.create(
                    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                    messages=smessages,
                    max_tokens=1024,
                )

                result = chat_completion.choices[0].message.content
            except Exception as e:
                print(e)
                fail = True
            messages.append({"role": "assistant", "content": result})
            if fail:
                messages = messages[:-2]

        self.db.upsert(
            {
                "key": str(self.get_udata_id(message)),
                "data": self.udata[self.get_udata_id(message)],
            },
            Query().key == self.get_udata_id(message),
        )

        self.cooldowns[message.guild.id] = time.time() + 10

        if len(result) > 900:
            for i in [result[i:i+900] for i in range(0, len(result), 900)]:
                await message.reply(i, allowed_mentions=discord.AllowedMentions.none())
            return

        await message.reply(result, allowed_mentions=discord.AllowedMentions.none())


def setup(bot):
    bot.add_cog(AICog(bot))
