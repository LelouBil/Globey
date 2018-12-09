import Globey
# import discord
import Globey.control as control
import discord.ext.commands


@discord.ext.commands.group( hidden=True)
@control.only_owner()
async def globe(ctx: discord.ext.commands.Context):
    if not control.isAdmin(ctx.message.author.id):
        return
    if ctx.invoked_subcommand is None:
        await discord.ext.commands.bot._default_help_command(ctx, "globe")


@globe.command(hidden=True)
@control.only_owner()
async def load(ctx, extension_name: str):
    """Loads an extension."""
    if not control.isAdmin(ctx.message.author.id):
        return
    try:
        Globey.client.load_extension(Globey._cogs_dir + "." + extension_name.lower())
    except (AttributeError, ImportError) as e:
        await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await ctx.send("{} loaded.".format(extension_name))


@globe.command(hidden=True)
@control.only_owner()
async def unload(ctx, extension_name: str):
    """Unloads an extension."""
    if not control.isAdmin(ctx.message.author.id):
        return
    Globey.client.unload_extension(Globey._cogs_dir + "." + extension_name.lower())
    await ctx.send("{} unloaded.".format(extension_name))
