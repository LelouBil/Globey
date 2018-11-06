import Globey
import discord.ext.commands

command = discord.ext.commands.command
client = Globey.client


class Control:

    @command(pass_context=True, hidden=True)
    async def shutdown(self,ctx):
        if ctx.message.author.id == "407938385190060044" or ctx.message.author.id == "388192128607584256" or ctx.message.author.id == "203874311696547851":
            await client.say("im shutting down, goodbye!")
            await client.logout()
        else:
            await client.say("too bad that you are not the bot master")


def setup(bot: discord.ext.commands.Bot):
    bot.add_cog(Control())
