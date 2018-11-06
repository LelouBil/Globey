import discord.ext.commands

import Globey

client = Globey.client
command = discord.ext.commands.command


class Info:
    @command(pass_context=True)
    async def userinfo(self,ctx, user: discord.User):  # notice how i added for mentioning user
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
        await client.say(embed=embed)

    @command(pass_context=True)
    async def ping(self,ctx):
        await client.say('Pong! :robot:')


def setup(bot):
    bot.add_cog(Info())