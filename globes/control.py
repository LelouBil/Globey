import Globey
import discord.ext.commands

command = discord.ext.commands.command
client = Globey.client
import Globey.control


class Control:

    @command(hidden=True)
    async def shutdown(self, ctx: discord.ext.commands.Context):
        if Globey.control.isAdmin(ctx.message.author):
            await ctx.send("im shutting down, goodbye!")
            await client.logout()
        else:
            await ctx.send("too bad that you are not the bot master")

    @command()
    async def hide(self, ctx, h: str):
        if Globey.control.isAdmin(ctx.message.author.id):
            if h:
                await client.change_presence(status=discord.Status.online)
            else:
                await client.change_presence(status=discord.Status.invisible)


def setup(bot: discord.ext.commands.Bot):
    bot.add_cog(Control())
