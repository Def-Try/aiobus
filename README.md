<div align="center">
    <h1>AiOBus</h1>
    <p>le bot from le googer</p>
</div>

> [!WARNING]
> Bot is in strong WiP stage. Do not expect much of it right now!

> [!NOTE]
> I'm looking for a new bot avatar. Suggest me one in DMs!

AiObus is an All-In-One bot designed to fulfill basically all of discord server needs and more - from simple automoderation to powerful server-state dumper and restorer.

![googer_](https://img.shields.io/badge/Author-googer__-blue?logo=discord&logoColor=white)
![GitHub top language](https://img.shields.io/github/languages/top/Def-Try/aiobus)
![GitHub License](https://img.shields.io/github/license/Def-Try/aiobus)

[Invite bot to your server](https://discord.com/oauth2/authorize?client_id=988117050222342194&permissions=1639603105782&scope=bot)


## Description

This bot was (and currently still is) originally just a small
little project that i made for fun. Now it is used on at
least 2 relatively big servers to entertain it's members
and I am aiming into making this a full-blown plug-and-play,
all-in-one discord bot for everything thay a server may ever
need.


# Cogs

Current list of "cogs" (modules):
* basic.py - Core cog.<br>
  Provides basic functionality like /help or /ping
  
* fun - "fun" commands cog.<br>
  Any fun commands that I was not sure to make another cog for.
  
* actions_commands.py - Actions cog.<br>
  One of the first cogs that have been written.
  Simple "send embed with gif" commands
  
* adminhelp.py - Adminhelp.<br>
  Simple ans instant modmail with integration with INTERCHAT
  
* interchat.py - Interchat.<br>
  Communication between two channels. Can link DM to a channel,
  VC channel to a chat, etc, you've got the idea.
  
* media.py - Media related.<br>
  Commands that are in any way related to media files.
  
* gpt.py - GPT Chat.<br>
  Makes so that when someone @pings a bot it will answer to
  the message with GPT AI. Includes a fairly simple prompt
  to make it follow certain laws. A few lawsets available.
  
* starboard.py - Starboard.<br>
  Simple starboard manager. Put enough stars on a message and
  it will be sent to a cool channel.
  
* nsfw.py - NSFW commands.<br>
  Simple cog that gives commands that search for NSFW content
  on rule34 or danbooru.
  
* util.py - Utility commands.<br>
  Commands that don't deserve another cog but could be useful
  by themselves.


# TODO

* moderation cog. with temp mutes/bans/etc
* update starboard. fix bot starboarding it's starboard messages, make it more configurable
