import discord.ext.commands
import discord
import Globey
import Globey.control
import sqlite3

command = discord.ext.commands.command
client = Globey.client
DB = Globey.DB


class Globaladmin:

    @command(pass_context=True)
    @Globey.control.only_owner()
    async def globalmute(self, ctx, member: discord.Member):
        try:
            DB.execute("INSERT INTO global_mutes (user_id) VALUES (?)", (member.id,))
            client.send_message(ctx.message.channel, "Done !")
        except sqlite3.IntegrityError:
            client.send_message(ctx.message.channel, "The user is already global-muted !")

    @command(pass_context=True)
    @Globey.control.only_owner()
    async def globalunmute(self, ctx, member: discord.Member):
        DB.execute("DELETE FROM global_mutes WHERE user_id=?", (member.id,))
        client.send_message(ctx.message.channel, "Done !")


def is_muted(name):
    res = DB.fetch("SELECT 1 FROM global_mutes WHERE user_id = ?", (name,))
    return len(res) > 0


def setup(bot):
    bot.add_cog(Globaladmin())
