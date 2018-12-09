import random
import discord.ext.commands

import Globey

client = Globey.client
command = discord.ext.commands.command


class Fun:

    @command()
    async def hi(self, ctx):
        await ctx.send("**Hello, human**")

    @command(hidden=True)
    async def master(self, ctx):
        if Globey.control.isAdmin(ctx.message.author.id):
            await ctx.send("Hi master :leaves:")
        else:
            await ctx.send("Hey wait a minute, you aren't my master!!! :scream:")

    @command()
    async def mood(self, ctx):
        mood = (random.choice([1, 2, 3, 4, ]))
        if mood == 1:
            await ctx.send("*Angry*")
        elif mood == 2:
            await ctx.send("*Annoyed*")
        elif mood == 3:
            await ctx.send("*Happy*")
        elif mood == 4:
            await ctx.send("*Sad*")


def setup(bot: discord.ext.commands.Bot):
    bot.add_cog(Fun())
