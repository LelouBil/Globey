import discord
import discord.ext.commands
import json
import Globey
import Globey.apicall as apicall

client = Globey.client


class Testing:

    @client.command()
    async def testCommand(self, ctx: discord.ext.commands.Context):
        pass


def setup(bot):
    bot.add_cog(Testing())
