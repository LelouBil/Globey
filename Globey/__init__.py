import os
import traceback
from os import listdir
from os.path import isfile, join
import Globey.control

import discord
import numpy as np
from discord.ext import commands

import Globey.GlobeyHelpFormatter
from Globey.extern.GloDB import GloDB


cogs_dir = "globes"

Client = discord.Client

client = commands.Bot(command_prefix="_", formatter=GlobeyHelpFormatter.GlobeyHelpFormatter())
DB = GloDB()
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
    control.onload()
    db = list(DB.get_all_servers())
    current = list(map(lambda s: s.id, client.servers))

    diff = np.setdiff1d(db, current)

    await remove_servers(diff)

    diff = np.setdiff1d(current, db)

    await add_servers(diff)
    update_counter()
    print("Bot Is Online!")


@client.event
async def on_server_join(server):
    DB.register_server(server)
    update_counter(1)


def update_counter(param: int = 0):
    global counter
    if counter == 0:
        counter = len(client.servers)
    else:
        counter += param
    client.change_presence(game=discord.Game(name=f"linking people on {counter} servers"))


@client.event
async def on_server_remove(server):
    DB.delete_server(int(server.id))
    update_counter(-1)

token = os.environ['GLOBEY_TOKEN']
import Globey.globe
for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            client.load_extension(cogs_dir + "." + extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()
client.run(token)
