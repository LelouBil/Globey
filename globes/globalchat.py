import discord.ext.commands

import Globey

client = Globey.client
command = discord.ext.commands.command

DB = Globey.DB

import re

mentionreg = re.compile("<@(\d+)>")

everyhere = re.compile("(@)(everyone|here)")

linkreg = re.compile("(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?")

class GlobalChat:
    @command(pass_context=True)
    async def globaldef(self, ctx):
        if DB.is_global(ctx.message.channel):
            await client.say("This channel is already global !")
            return
        await client.say("this channel is now set as a global channel")
        channel = ctx.message.channel  # here I get the channel
        DB.register_channel(channel)

    @command(pass_context=True)
    async def globalstop(self, ctx):
        if not DB.is_global(ctx.message.channel):
            await client.say("This channel is not global !")
            return
        await client.say("this channel is not anymore set as a global channel")
        channel = ctx.message.channel
        DB.unregister_channel(channel)

    async def filterMessage(self,content: str):
        matchobj = mentionreg.search(content)
        if matchobj is not None:
            toreplace = matchobj.group()
            id = matchobj.group(1)
            print("mention of : " + id + " ---- " + toreplace)
            user = await client.get_user_info(str(id))
            username = str(user)
            content = content.replace(toreplace, username)
            # fin mentions

        # links

        match = linkreg.search(content)
        if match is not None:
            link = match.group()
            content = content.replace(link, "_[link are disabled here]_")

        # everyHere

        ma = everyhere.search(content)
        if ma is not None:
            tore = ma.group(1)
            ot = ma.group(2)
            # print("mention of : " + id + " ---- " + toreplace)
            content = content.replace(ma.group(), tore + " " + ot)
            # fin mentions
        return content

    # @client.event
    async def on_message(self, message : discord.client.Message):
        if DB.is_global(message.channel):
            cmds = client.commands.keys()
            if not str(message.content).startswith(client.command_prefix)\
                    and not \
                    cmds.__contains__(str(message.content).replace(client.command_prefix, "", 1)):
                filtered = await self.filterMessage(message.content)
                if not message.author.bot:
                    channel = DB.get_global_channels()
                    for i in channel:
                        if i.type != discord.channel.ChannelType.private:
                            try:
                                await client.send_message(i, f"**[{message.author}@{message.server}]** {filtered}")
                            except discord.errors.Forbidden:
                                print(f"forbidden channel : {i.name}@{i.server.name}")


def setup(bot):
    bot.add_cog(GlobalChat())
