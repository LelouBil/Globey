import discord.ext.commands
import Globey

client = Globey.client
command = discord.ext.commands.command


class Other:
    @command(pass_context=True)
    async def hi(self, ctx):
        await client.say("**Hello, human**")

    @command(pass_context=True)
    async def redriot(self, ctx):
        await client.say("is my **creator**")

    @command(pass_context=True, hidden=True)
    async def master(self, ctx):
        if ctx.message.author.id == "407938385190060044" or ctx.message.author.id == "388192128607584256" or ctx.message.author.id == "203874311696547851":
            await client.say("Hi master :leaves:")
        else:
            await client.say("Hey wait a minute, you aren't my master!!! :scream:")

    @command(pass_context=True)
    async def server(self, ctx):
        await client.say("https://discord.gg/Gt5nF5T")

    @command(pass_context=True)
    async def amiuseful(self, ctx):
        await client.say("Yes, as every member of the sect you were choosen by ***me***")

    @command(pass_context=True)
    async def invite(self, ctx):
        await client.say(
            "https://discordapp.com/api/oauth2/authorize?client_id=456478882577645568&permissions=8&scope=bot")


def setup(bot):
    bot.add_cog(Other())
