import discord.ext.commands

import Globey

client = Globey.client
command = discord.ext.commands.command


class Info:

    @command()
    async def ping(self, ctx):
        await ctx.send('Pong! :robot:')

    @command()
    async def userinfo(self, ctx, user: discord.User):  # notice how i added for mentioning user
        embed = discord.Embed(title="User Info for {}".format(user.name), color=user.color)
        embed.add_field(name="Username:", value=user.name, inline=True)
        embed.add_field(name="User ID:", value=user.id, inline=True)
        embed.add_field(name="Is Bot:", value=user.bot)
        embed.add_field(name="Created at:", value=user.created_at, inline=True)
        embed.add_field(name="Nickname:", value=user.display_name)
        embed.add_field(name="Status:", value=user.status, inline=True)
        embed.add_field(name="Playing:", value=user.game)
        embed.add_field(name="Highest Role:", value=user.top_role, inline=True)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @command()
    async def guild(self, ctx):
        await ctx.send("https://discord.gg/3PPhfsf")

    @command()
    async def invite(self, ctx):
        await ctx.send(
            "https://discordapp.com/api/oauth2/authorize?client_id=456478882577645568&permissions=8&scope=bot")


def setup(bot):
    bot.add_cog(Info())
