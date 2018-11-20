import os
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

cogs_dir = "globes"
log = logging.getLogger(__name__)
logLevel = logging._nameToLevel[os.getenv('GLOBEY_LOGLEVEL', 'INFO')]
logging.basicConfig(level=logLevel)
Client = discord.Client
token = os.environ['GLOBEY_TOKEN']
client = commands.Bot(command_prefix="_", formatter=GlobeyHelpFormatter.GlobeyHelpFormatter())
DB = GloDB()
initTime = 5
counter = 0


async def remove_servers(diff):
    for s in diff:
        DB.delete_server(int(s))


async def add_servers(diff):
    for s in diff:
        sarv = client.get_server(s)
        DB.register_server(sarv)


@client.event
async def on_ready():
    log.info("Bot starting...")
    await client.change_presence(status=discord.Status.invisible)
    log.info("Loading Control module")
    control.onload()
    log.info("Checking server lists")
    db = list(DB.get_all_servers())
    current = list(map(lambda s: s.id, client.servers))

    diff = np.setdiff1d(db, current)
    if len(diff) == 0:
        log.info("No servers to remove from DB")
    else:
        log.info("Removing servers from DB")
        await remove_servers(diff)

    diff = np.setdiff1d(current, db)
    if len(diff) == 0:
        log.info("No servers to add from DB")
    else:
        log.info("Adding servers from DB")
        await add_servers(diff)

    log.info("Checking global channels")
    for c in DB.get_global_channels():
        log.debug("Checking : " + c.name + "@" + c.server.name)
        await globes.globalchat.GlobalChat.ensureWebHook(c.id)
    log.info("Updating server count")
    await update_counter()
    log.info("Waiting %s seconds",initTime)
    time.sleep(initTime)
    await client.change_presence(status=discord.Status.online)
    log.info("Bot is online")


@client.event
async def on_server_join(server):
    log.info("Bot has joined server %s", server.name)
    DB.register_server(server)
    await update_counter(1)


async def update_counter(param: int = 0):
    global counter
    if counter == 0:
        counter = len(client.servers)
    else:
        counter += param
    await client.change_presence(game=discord.Game(name=f"linking people on {counter} server{'s' if counter > 1 else ''}"))


@client.event
async def on_server_remove(server):
    log.info("Bot removed from server %s", server.name)
    DB.delete_server(int(server.id))
    await update_counter(-1)


log.info("Loading extentions...")
for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
    try:
        log.info("Loading %s", cogs_dir + "." + extension)
        client.load_extension(cogs_dir + "." + extension)
        log.debug("Loaded")
    except Exception as e:
        log.error(f'Failed to load extension {extension}.')
        traceback.print_exc()

log.info("Running client")
client.run(token)
