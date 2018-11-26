import Globey
import discord.ext.commands

client = Globey.client
command = discord.ext.commands.command


class Game:
    # @command(pass_context=True)
    async def start(self,ctx):
        await client.say(
            "**This is a RPG dueling mode game:**\n *to pick a class do `_select[class name]` Ex: `_selectdemonhunter`* **\n Exorcist \n Mage \n Necromancer \n Wizard \n Samurai \n Demon Hunter \n ***!Warning!***  you can't change your class**")

        @command(pass_context=True)
        async def selectmage(self,ctx):
            await client.say("you selected **Mage** class")

        @command(pass_context=True)
        async def selectexorcist(self,ctx):
            await client.say("you selected **Exorcist** class")

        @command(pass_context=True)
        async def selectdemonhunter(self,ctx):
            await client.say("you selected **Demon Hunter** class")

        @command(pass_context=True)
        async def selectsamurai(self,ctx):
            await client.say("you selected **Samurai** class")

        @command(pass_context=True)
        async def selectwizard(self,ctx):
            await client.say("you selected **Wizard** class")

        @command(pass_context=True)
        async def selectnecromancer(self,ctx):
            await client.say("you selected **Necromancer** class")


def setup(bot):
    bot.add_cog(Game())
