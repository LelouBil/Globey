import discord.ext.commands
import discord
import Globey
import Globey.control
import sqlite3
import globes.globalchat

command = discord.ext.commands.command
client = Globey.client
DB = Globey.DB


class Globaladmin:

    @command()
    @Globey.control.only_owner()
    async def globalmute(self, ctx, *, member: str):
        us = next(filter(lambda x: str(x) == member, client.get_all_members()), None)
        try:
            DB.execute("INSERT INTO global_mutes (user_id) VALUES (?)", (us.id,))
            await client.add_reaction(ctx.message, u"\U0001F44C")

        except sqlite3.IntegrityError:
            await client.send_message(ctx.message.channel, "The user is already globally-muted !")

    @command()
    @Globey.control.only_owner()
    async def globalunmute(self, ctx, *,member: str):
        us = next(filter(lambda x: str(x) == member, client.get_all_members()), None)
        DB.execute("DELETE FROM global_mutes WHERE user_id=?", (us.id,))
        await client.add_reaction(ctx.message, u"\U0001F44C")

    @command()
    @Globey.control.only_owner()
    async def globallock(self,ctx):
        globes.globalchat.globalLock = True
        channel = DB.get_global_channels()
        for i in channel:
            await client.send_message(i, "The global chat has been locked by an owner of the bot")
            await client.send_message(i, "Any message sent will not be forwarded until the global chat is unlocked")

    @command()
    @Globey.control.only_owner()
    async def globalunlock(self,ctx):
        globes.globalchat.globalLock = False
        channel = DB.get_global_channels()
        for i in channel:
            await client.send_message(i, "The global chat is now unlocked")
            await client.send_message(i, "Messages will now be forwared again")


def is_muted(name):
    res = DB.fetch("SELECT 1 FROM global_mutes WHERE user_id = ?", (name,))
    return len(res) > 0


def setup(bot):
    bot.add_cog(Globaladmin())
