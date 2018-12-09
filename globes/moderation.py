import discord.ext.commands

import Globey

client = Globey.client
command = discord.ext.commands.command

# TODO redo this entirely
class Moderation:
    @command()
    async def kick(self, ctx, user: discord.User, *, reason: str):
        if "452930924015910913" in [role.id for role in ctx.message.author.roles]:
            await client.kick(user)
            await ctx.send(f"*!!!*, user **has been kicked for reason:** {reason}*!!!*")

    @command()
    async def ban(self, ctx, user: discord.Member):
        if "452930924015910913" in [role.id for role in ctx.message.author.roles]:
            await client.ban(user)
            await ctx.send(f"{user.name} **Has been Banned!** Goodbye hope we won't see you again.")

    @command()
    async def warn(self, ctx, user: discord.Member):
        if "452930924015910913" in [role.id for role in ctx.message.author.roles]:
            embed = discord.Embed(title="WARNING!",
                                  description="Please be sure to read Rules so you don't break anything again!",
                                  color=0xFFF000)
            embed.add_field(name=f"{user.name} Has been Warned", value="*Warn*")
            await ctx.send("done")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation())
