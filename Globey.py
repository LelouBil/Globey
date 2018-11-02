import asyncio
import discord
from discord.ext import commands
import sqlite3
import random

import time

Client = discord.Client
client = commands.Bot(command_prefix="_")

sqlite = sqlite3.connect("/storage/database.db")
cursor = sqlite.cursor()
cursor.execute("""

CREATE TABLE IF NOT EXISTS servers
(
 `server_id`   int NOT NULL,
 `server_name` text NOT NULL ,

PRIMARY KEY (`server_id`)
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS global_channels (
    channel_id integer NOT NULL,
    server_id integer NOT NULL
, channel_name TEXT NOT NULL,
PRIMARY KEY (`channel_id`),
FOREIGN KEY(server_id) REFERENCES servers(server_id)
);
""")


def getCursor():
    return sqlite.cursor()


def register_server(srv: discord.server.Server):
    name = srv.name
    idd = srv.id
    getCursor().execute("INSERT INTO servers (server_id,server_name) VALUES (?,?)", (idd, name))
    sqlite.commit()


def register_channel(chan: discord.server.Channel):
    name = chan.name
    idd = chan.id
    srvid = chan.server.id
    getCursor().execute("INSERT INTO global_channels (channel_id,channel_name,server_id) VALUES (:id,:name,:srvid)",
                        {"id": idd, "name": name, "srvid": srvid})
    sqlite.commit()


def unregister_channel(chan: discord.server.Channel):
    idd = chan.id
    getCursor().execute(f"DELETE FROM global_channels WHERE channel_id=:id", {"id": idd})
    sqlite.commit()


def registered(srv: discord.server.Server):
    c = getCursor()
    c.execute(f"SELECT EXISTS(SELECT 1 FROM servers WHERE server_id={srv.id})")
    return c.fetchone() == (1,)


@client.event
async def on_ready():
    print("Bot Is Online!")
    for srv in client.servers:
        if not registered(srv):
            print("registering server : " + srv.name)
            register_server(srv)
    await client.change_presence(game=discord.Game(name="linking people"))


@client.command(pass_context=True)
async def mood(ctx):
    mood = (random.choice([1, 2, 3, 4, ]))
    if mood == 1:
        await client.say("*Angry*")
    elif mood == 2:
        await client.say("*Annoyed*")
    elif mood == 3:
        await client.say("*Happy*")
    elif mood == 4:
        await client.say("*Sad*")


@client.command(pass_context=True)
async def ping(ctx):
    await client.say('Pong! :robot:')


@client.command(pass_context=True, hidden=True)
async def shutdown(ctx):
    if ctx.message.author.id == "407938385190060044" or ctx.message.author.id == "388192128607584256" or ctx.message.author.id == "203874311696547851":
        await client.say("im shutting down, goodbye!")
        await client.logout()
    else:
        await client.say("too bad that you are not the bot master")


@client.command(pass_context=True)
async def userinfo(ctx, user: discord.User):  # notice how i added for mentioning user
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


@client.command(pass_context=True)
async def hi(ctx):
    await client.say("**Hello, human**")


@client.command(pass_context=True)
async def start(ctx):
    await client.say(
        "**This is a RPG dueling mode game:**\n *to pick a class do `_select[class name]` Ex: `_selectdemonhunter`* **\n Exorcist \n Mage \n Necromancer \n Wizard \n Samurai \n Demon Hunter \n ***!Warning!***  you can't change your class**")

    @client.command(pass_context=True)
    async def selectmage(ctx):
        await client.say("you selected **Mage** class")

    @client.command(pass_context=True)
    async def selectexorcist(ctx):
        await client.say("you selected **Exorcist** class")

    @client.command(pass_context=True)
    async def selectdemonhunter(ctx):
        await client.say("you selected **Demon Hunter** class")

    @client.command(pass_context=True)
    async def selectsamurai(ctx):
        await client.say("you selected **Samurai** class")

    @client.command(pass_context=True)
    async def selectwizard(ctx):
        await client.say("you selected **Wizard** class")

    @client.command(pass_context=True)
    async def selectnecromancer(ctx):
        await client.say("you selected **Necromancer** class")


@client.command(pass_context=True)
async def kick(ctx, user: discord.User, *, reason: str):
    if "452930924015910913" in [role.id for role in ctx.message.author.roles]:
        await client.kick(user)
        await client.say(f"*!!!*, user **has been kicked for reason:** {reason}*!!!*")


@client.command(pass_context=True)
async def ban(ctx, user: discord.Member):
    if "452930924015910913" in [role.id for role in ctx.message.author.roles]:
        await client.ban(user)
        await client.say(f"{user.name} **Has been Banned!** Goodbye hope we won't see you again.")


@client.command(pass_context=True)
async def warn(ctx, user: discord.Member):
    if "452930924015910913" in [role.id for role in ctx.message.author.roles]:
        embed = discord.Embed(title="WARNING!",
                              description="Please be sure to read Rules so you don't break anything again!",
                              color=0xFFF000)
        embed.add_field(name=f"{user.name} Has been Warned", value="*Warn*")
        await client.say("done")
        await client.say(embed=embed)


@client.command(pass_context=True)
async def redriot(ctx):
    await client.say("is my **creator**")


@client.command(pass_context=True, hidden=True)
async def master(ctx):
    if ctx.message.author.id == "407938385190060044" or ctx.message.author.id == "388192128607584256" or ctx.message.author.id == "203874311696547851":
        await client.say("Hi master :leaves:")
    else:
        await client.say("Hey wait a minute, you aren't my master!!! :scream:")


@client.command(pass_context=True)
async def server(ctx):
    await client.say("https://discord.gg/Gt5nF5T")


@client.command(pass_context=True)
async def amiuseful(ctx):
    await client.say("Yes, as every member of the sect you were choosen by ***me***")


@client.command(pass_context=True)
async def spam(ctx):
    await client.say(" ")
    await client.say(" ")
    await client.say(" ")


@client.command(pass_context=True)
async def globaldef(ctx):
    if isglobal(ctx.message.channel):
        await client.say("This channel is already global !")
        return
    await client.say("this channel is now set as a global channel")
    channel = ctx.message.channel  # here I get the channel
    register_channel(channel)


@client.command(pass_context=True)
async def globalstop(ctx):
    if not isglobal(ctx.message.channel):
        await client.say("This channel is not global !")
        return
    await client.say("this channel is not anymore set as a global channel")
    channel = ctx.message.channel
    unregister_channel(channel)


@client.command(pass_context=True)
async def invite(ctx):
    await client.say("https://discordapp.com/api/oauth2/authorize?client_id=456478882577645568&permissions=8&scope=bot")


def getGlobalChannels():
    c = getCursor()
    c.execute("SELECT * FROM global_channels")
    rows = c.fetchall()
    channels = list()
    for row in rows:
        cid = row[0]
        sid = row[1]
        chanel = client.get_server(str(sid)).get_channel(str(cid))
        channels.append(chanel)
    return channels


def isglobal(channel: discord.channel.Channel):
    c = getCursor()
    c.execute(f"SELECT EXISTS(SELECT 1 FROM global_channels WHERE channel_id={channel.id})")
    return c.fetchone() == (1,)


noRepeat = {"_globaldef", "_globalstop"}

# regexes
import re

mentionreg = re.compile("<@(\d+)>")

everyhere = re.compile("(@)(everyone|here)")

linkreg = re.compile("(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?")


async def filterMessage(content: str):
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

    #everyHere

    ma = everyhere.search(content)
    if ma is not None:
        tore = ma.group(1)
        ot = ma.group(2)
        #print("mention of : " + id + " ---- " + toreplace)
        content = content.replace(ma.group(), tore + " " + ot)
        # fin mentions
    return content


@client.event
async def on_message(message):
    if isglobal(message.channel):
        if not noRepeat.__contains__(message.content):
            filtered = await filterMessage(message.content)
            if not message.author.bot:
                channel = getGlobalChannels()
                for i in channel:
                    if i.type != discord.channel.ChannelType.private:
                        try:
                            await client.send_message(i, f"**[{message.author}@{message.server}]** {filtered}")
                        except discord.errors.Forbidden:
                            print(f"forbidden channel : {i.name}@{i.server.name}")

    if message.content.startswith("cookie"):
        await client.add_reaction(message,"\N{COOKIE}")
    if message.content.startswith("hello"):
        embed1 = discord.Embed(title="Hello :wave:", description=f"Hello {message.author.name}, How are you?",
                               color=message.author.color)
        embed1.set_thumbnail(url=message.author.avatar_url)
        embed1.set_footer(text="send by god")
        await client.send_message(message.channel, embed=embed1)
    if message.content.find(':EmojiName:'):
        for i in client.get_all_emojis():
            if i.id == '#EmojiID#':
                return await client.add_reaction(message.channel, i)
    if message.content.startswith("help"):
        embed2 = discord.Embed(title="**Help menu**",
                               description=f"**Hello {message.author.name}, here are all comands (with prefix_):** \n hi, invite, server, redriot, amiuseful, spam, invite. \n **admin command:**\n ban, warn, kick",
                               color=message.author.color)
        embed2.set_thumbnail(url=message.author.avatar_url)
        embed2.set_footer(text="send by god")
        await client.send_message(message.channel, embed=embed2)
    if message.content.startswith("party"):
        await client.add_reaction(message,"\N{TADA}")
    if message.content.startswith("lol"):
        await client.add_reaction(message,"\N{ROLF}")
    if message.content.startswith("no"):
        await client.add_reaction(message,"\N{FACEPALM}")
    await client.process_commands(message)


client.run("NDU2NDc4ODgyNTc3NjQ1NTY4.DryxQw.aP1IANFsvekqP8yHnvvEbaBy3wE")  # token (secret)
