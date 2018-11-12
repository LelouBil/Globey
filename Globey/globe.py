import Globey
# import discord
import Globey.control as control
import discord.ext.commands

client = Globey.client


@client.group(pass_context=True)
async def globe(ctx: discord.ext.commands.Context):
    if not control.isAdmin(str(ctx.message.author.id)):
        return
    if ctx.invoked_subcommand is None:
        await discord.ext.commands.bot._default_help_command(ctx, "globe")


@globe.command(pass_context=True)
async def load(ctx,extension_name: str):
    """Loads an extension."""
    if not control.isAdmin(str(ctx.message.author.id)):
        return
    try:
        client.load_extension(Globey.cogs_dir + "." + extension_name.lower())
    except (AttributeError, ImportError) as e:
        await client.say("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        return
    await client.say("{} loaded.".format(extension_name))


@globe.command(pass_context=True)
async def unload(ctx,extension_name: str):
    """Unloads an extension."""
    if not control.isAdmin(str(ctx.message.author.id)):
        return
    client.unload_extension(Globey.cogs_dir + "." + extension_name.lower())
    await client.say("{} unloaded.".format(extension_name))
