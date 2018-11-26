import random
import discord.ext.commands

import Globey

client = Globey.client
command = discord.ext.commands.command


class Fun:

    @command(pass_context=True)
    async def hi(self, ctx):
        await client.say("**Hello, human**")

    @command(pass_context=True, hidden=True)
    async def master(self, ctx):
        if Globey.control.isAdmin(ctx.message.author.id):
            await client.say("Hi master :leaves:")
        else:
            await client.say("Hey wait a minute, you aren't my master!!! :scream:")

    @command(pass_context=True)
    async def mood(self, ctx):
        mood = (random.choice([1, 2, 3, 4, ]))
        if mood == 1:
            await client.say("*Angry*")
        elif mood == 2:
            await client.say("*Annoyed*")
        elif mood == 3:
            await client.say("*Happy*")
        elif mood == 4:
            await client.say("*Sad*")


def setup(bot: discord.ext.commands.Bot):
    bot.add_cog(Fun())
