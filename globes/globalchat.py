from typing import Optional

import discord.ext.commands
import logging
import Globey
import Globey.apicall as apicall
import requests
import globes
import json

from globes import ServerAdmin, globaladmin

client = Globey.client
log = logging.getLogger("Global-Chat")
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
            log.error(f"an error occured, cannot list webhooks of channel {channel}")
            log.error(e.stacktrace())
            await client.send_message(client.get_channel(channel),
                                      "Hey, for the new version of the Global chat I need the **manage webhooks** "
                                      "permission for this channel !" +
                                      "\nPlease add it, and then do `_globalstop` and `_globaldef` again !" +
                                      "\nYou can also just ignore this message, and the global chat will work the "
                                      "same way as before."
                                      )
            return False

    @command(pass_context=True)
    @ServerAdmin.only_admin()
    async def nosend(self, ctx, b: bool):
        DB.set_preference(ctx.message.channel.server.id, "nosend", str(b))

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
    @ServerAdmin.only_admin()
    async def globaldef(self, ctx):
        if DB.is_global(ctx.message.channel):
            await client.say("This channel is already global !")
            return
        await client.say("this channel is now set as a global channel")
        channel = ctx.message.channel  # here I get the channel
        DB.register_channel(channel)
        await self.ensureWebHook(channel.id)

    @command(pass_context=True)
    @ServerAdmin.only_admin()
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
            if globaladmin.is_muted(message.author.id):
                return
            if not str(message.content).startswith(client.command_prefix) \
                    and not \
                    cmds.__contains__(str(message.content).replace(client.command_prefix, "", 1)):
                filtered = await self.filterMessage(message.content)
                if not message.author.bot:
                    channel = DB.get_global_channels()
                    for i in channel:
                        if i.type != discord.channel.ChannelType.private:
                            try:
                                if i.id == message.channel.id:
                                    if DB.get_preference(message.server.id, "nosend") == "True":
                                        continue
                                hook = await GlobalChat.getwebhook(i.id)
                                name = message.author.name + "@[" + message.server.name + "]"
                                content = filtered
                                av = message.author.avatar_url
                                hook.send_message(name, content, av)
                            except discord.errors.Forbidden:
                                print(f"forbidden channel : {i.name}@{i.server.name}")
                            except Globey.apicall.ApiError:
                                await client.send_message(i, f"**[{message.author}@{message.server}]** {filtered}")


class WebHook:
    id: str
    token: str
    name: str

    def __init__(self, id, token) -> None:
        self.id = id
        self.token = token

    def getname(self):
        pass  # todo

    def send_message(self, name: str, message: str, avatar: str):
        apicall.post_endpoint(f"webhooks/{self.id}/{self.token}", {
            "content": message,
            "avatar_url": avatar,
            "username": name
        })


def setup(bot):
    bot.add_cog(GlobalChat())
