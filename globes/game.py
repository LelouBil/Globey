import Globey
import discord.ext.commands

client = Globey.client
command = discord.ext.commands.command


class Game:
    # @command()
    async def start(self,ctx):
        await ctx.send(
            "**This is a RPG dueling mode game:**\n *to pick a class do `_select[class name]` Ex: `_selectdemonhunter`* **\n Exorcist \n Mage \n Necromancer \n Wizard \n Samurai \n Demon Hunter \n ***!Warning!***  you can't change your class**")

        @command()
        async def selectmage(self,ctx):
            await ctx.send("you selected **Mage** class")

        @command()
        async def selectexorcist(self,ctx):
            await ctx.send("you selected **Exorcist** class")

        @command()
        async def selectdemonhunter(self,ctx):
            await ctx.send("you selected **Demon Hunter** class")

        @command()
        async def selectsamurai(self,ctx):
            await ctx.send("you selected **Samurai** class")

        @command()
        async def selectwizard(self,ctx):
            await ctx.send("you selected **Wizard** class")

        @command()
        async def selectnecromancer(self,ctx):
            await ctx.send("you selected **Necromancer** class")


def setup(bot):
    bot.add_cog(Game())
