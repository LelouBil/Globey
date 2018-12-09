import discord.ext.commands
import discord
import Globey
import Globey.control

has_permissions = discord.ext.commands.has_permissions
command = discord.ext.commands.command
client = Globey.client
DB = Globey.DB


def is_admin(member: discord.Member):
    srid = member.guild.id
    roleid = DB.get_preference(srid, "admin_role")
    if roleid == "" or roleid == "0":
        if member.guild_permissions.administrator:
            return True
        else:
            return False
    for r in member.roles:
        if r.id == roleid:
            return True
    return False


def only_admin():
    def predicate(ctx):
        return is_admin(ctx.message.author)

    return discord.ext.commands.check(predicate)


class GuildAdmin:

    @command()
    @has_permissions(administrator=True)
    async def setAdminRole(self, ctx: discord.ext.commands.Context, role_id: str):
        guild = ctx.guild.id
        DB.set_preference(guild, "admin_role", role_id)
        await ctx.send("Done !")

    # @command()
    @only_admin()
    async def admincommand(self, ctx):
        await client.send_message(ctx.message.channel, "heya")


def setup(bot):
    bot.add_cog(GuildAdmin())
