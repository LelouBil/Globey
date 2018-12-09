import inspect
import os
import sentry_sdk

sentry_sdk.init("https://82d45e810e57456da9fd8f8198f86f80@sentry.io/1340390")
import traceback
from os import listdir
from os.path import isfile, join
import Globey.control
import globes as globes
import discord
import time
import numpy as np
import logging

from discord.ext import commands

import Globey.GlobeyHelpFormatter
import Globey.globe
from Globey.extern.GloDB import GloDB

# LOG SETUP
_logLevel = os.getenv('GLOBEY_LOGLEVEL', 'INFO')
logging.basicConfig(level=_logLevel)


def l() -> logging.Logger:
    stack = inspect.stack()
    loc: list = stack[1][0].f_locals
    if loc.__contains__("self"):
        the_class: str = loc["self"].__class__.__name__
    else:
        the_class: str = loc["__name__"]
    the_class = the_class.replace("__main__.", "")
    return logging.getLogger(the_class)


# bot setup
DB = GloDB()
_cogs_dir = "globes"
# pas utile // name = os.getenv("GLOBEY_USERNAME", 'Globey#9271')
_initTime = os.getenv('GLOBEY_INIT_TIME', 5)
_token = os.environ['GLOBEY_TOKEN']


class GlobeyClient(commands.Bot):
    initTime = 5
    counter = 0

    def __init__(self, initTime):
        self.initTime = initTime
        self.log = l()
        commands.Bot.__init__(self, command_prefix="_", formatter=GlobeyHelpFormatter.GlobeyHelpFormatter())

    async def remove_guilds(self, diff):
        for s in diff:
            DB.delete_guild(int(s))

    async def add_guilds(self, diff):
        for s in diff:
            sarv = self.get_guild(s)
            DB.register_guild(sarv)

    async def on_command_error(self, context: discord.ext.commands.Context, exception):
        cog = context.cog
        scope: sentry_sdk.Scope
        with sentry_sdk.configure_scope() as scope:
            u = {
                "id": context.author.id,
                "username": str(context.author),
                "type": "Member"
            }
            scope.user = u

            scope.set_tag("guild_id", context.guild.id)
            scope.set_tag("guild_name", context.guild.name)
            scope.set_tag("testing", True if os.environ.get("GLOBEY_TEST") else False)
            scope.set_tag("command", context.command.name)
            scope.set_tag("type", type(exception))

            fin = ["{{ default }}", context.command.name]
            if cog:
                fin.append(cog)
                scope.set_tag("globe", cog)
            scope.fingerprint = fin
            trace = traceback.format_exception(type(exception), exception, exception.__traceback__)
            l().error(f"Error in command {context.command}")
            l().error("".join(trace))

    async def on_ready(self):
        self.log.info("Connection ready, Bot starting...")
        await self.change_presence(status=discord.Status.invisible)
        self.log.info("Loading Control module")
        control.onload()
        self.log.info("Loading globes")
        await self.load_globes()
        self.log.info("Checking guild lists")
        db = list(DB.get_all_guilds())
        current = list(map(lambda s: s.id, client.guilds))

        diff = np.setdiff1d(db, current)
        if len(diff) == 0:
            self.log.info("No guilds to remove from DB")
        else:
            self.log.info("Removing guilds from DB")
            await self.remove_guilds(diff)

        diff = np.setdiff1d(current, db)
        if len(diff) == 0:
            self.log.info("No guilds to add from DB")
        else:
            self.log.info("Adding guilds from DB")
            await self.add_guilds(diff)

        self.log.info("Checking global channels")
        for c in DB.get_global_channels():
            self.log.debug("Checking : " + c.name + "@" + c.guild.name)
            await globes.globalchat.GlobalChat.ensureWebHook(c.id)
        self.log.info("Updating guild count")
        await self.update_counter()
        self.log.info("Waiting %s seconds", self.initTime)
        time.sleep(self.initTime)
        await client.change_presence(status=discord.Status.online)
        await self.update_counter()
        self.log.info("Bot is online")

    async def on_guild_join(self, guild):
        self.log.info("Bot has joined guild %s", guild.name)
        DB.register_guild(guild)
        await self.update_counter(1)

    async def update_counter(self, param: int = 0):
        if self.counter == 0:
            counter = len(client.guilds)
        else:
            self.counter += param
        await client.change_presence()
        await client.change_presence(
            activity=discord.Game(name=f"linking people on {counter} guild{'s' if counter > 1 else ''}"))

    async def on_guild_remove(self, guild):
        self.log.info("Bot removed from guild %s", guild.name)
        DB.delete_guild(int(guild.id))
        await self.update_counter(-1)

    async def load_globes(self):
        file = "globes.default"  # Todo configuration
        self.log.debug("Filename : " + file)
        with open(file, "r+") as f:
            for line in f:
                line = line.replace("\n", "")
                if line.startswith("#"):
                    self.log.info("Skipping disabled module " + line)
                    continue
                self.log.debug("Loading module : " + line)
                try:
                    client.load_extension(_cogs_dir + "." + line)
                    self.log.debug("Loaded")
                except Exception as e:
                    self.log.error(f'Failed to load extension {line}.')
                    traceback.print_exc()


l().info("Running client")
client = GlobeyClient(_initTime)
client.run(_token)
