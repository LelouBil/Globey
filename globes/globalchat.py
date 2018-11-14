from typing import Optional

import discord.ext.commands

import Globey
import Globey.apicall as apicall
import globes
import json

client = Globey.client
command = discord.ext.commands.command

DB = Globey.DB

import re

webhookName = "GlobalWebHook"

mentionreg = re.compile("<@(\d+)>")

everyhere = re.compile("(@)(everyone|here)")

linkreg = re.compile("(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?")


class GlobalChat:
    @staticmethod
    async def haswebhook(channel: str) -> bool:
        id = (await GlobalChat.getwebhook(channel)).id
        if id == "0":
            return False
        else:
            return True

    @staticmethod
    async def ensureWebHook(channel: str) -> bool:
        token: str
        id: str = ""
        if await GlobalChat.haswebhook(channel):
            try:
                hook = await GlobalChat.getwebhook(channel)
                rep = apicall.get_endpoint("/webhooks/" + str(hook.id) + "/" + str(hook.token))
                return True
            except apicall.ApiError:
                pass
        try:
            rep = apicall.get_endpoint("/channels/" + channel + "/webhooks")
            data = json.loads(rep.content)
            for d in data:
                if d["name"] == webhookName:
                    token = d["token"]
                    id = d["id"]
                    break
            if id == "":
                await GlobalChat.addwebhook(channel)
                return True
            DB.execute("UPDATE global_channels SET webhook_id=:wid, webhook_token=:wtoken WHERE channel_id =:cid",
                       {"wid": id, "wtoken": token, "cid": channel})
            return True
        except apicall.ApiError as e:
            client.say("an error occured")
            print(e.stacktrace())
            return False

    @staticmethod
    async def addwebhook(channel: str):
        try:
            rep = apicall.post_endpoint("/channels/" + channel + "/webhooks", data={"name": webhookName})
        except apicall.ApiError as e:
            client.say("an error occured")
            print(e.stacktrace())
            return
        data = json.loads(rep.content)
        id = data["id"]
        DB.get_cursor().execute("""UPDATE global_channels SET webhook_id=:wid ,webhook_token=:wtoken 
        WHERE channel_id=:cid""", {"wid": id, "wtoken": data["token"], "cid": channel})
        DB.sqlite.commit()
        return id

    @staticmethod
    async def delwebhook(channel: str):
        id = (await GlobalChat.getwebhook(channel)).id
        DB.execute("UPDATE global_channels SET webhook_id=:wid, webhook_token=:wtoken WHERE channel_id=:cid",
                   {"wid": 0, "wtoken": 0, "cid": channel})
        try:
            apicall.delete_endpoint("webhooks/" + str(id) + "/")
        except apicall.ApiError as e:
            client.say("an error occured")
            print(e.stacktrace())

    @staticmethod
    async def getwebhook(channel: str):
        if channel is discord.Channel:
            channel = channel.id

        rows = DB.fetch("SELECT webhook_id,webhook_token FROM global_channels WHERE channel_id = ?", (channel,))
        if len(rows) < 1:
            return None
        row = rows[0]
        id = row[0]
        token = row[1]
        return WebHook(id, token)

    @command(pass_context=True)
    async def globaldef(self, ctx):
        if DB.is_global(ctx.message.channel):
            await client.say("This channel is already global !")
            return
        await client.say("this channel is now set as a global channel")
        channel = ctx.message.channel  # here I get the channel
        DB.register_channel(channel)
        await self.addwebhook(channel.id)

    @command(pass_context=True)
    async def globalstop(self, ctx):
        if not DB.is_global(ctx.message.channel):
            await client.say("This channel is not global !")
            return
        await client.say("this channel is not anymore set as a global channel")
        channel = ctx.message.channel
        DB.unregister_channel(channel)
        await self.delwebhook(channel.id)

    async def filterMessage(self, content: str):
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
    async def on_message(self, message: discord.client.Message):
        if DB.is_global(message.channel):
            cmds = client.commands.keys()
            if not str(message.content).startswith(client.command_prefix) \
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


class WebHook:
    id: str
    token: str
    name: str

    def __init__(self, id, token) -> None:
        self.id = id
        self.token = token

    def getname(self):
        pass  # todo


def setup(bot):
    bot.add_cog(GlobalChat())
