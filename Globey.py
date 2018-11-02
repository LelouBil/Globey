import asyncio
import discord
from discord.ext import commands
import sqlite3
import random

import time

Client = discord.Client
client = commands.Bot(command_prefix="_")

sqlite = sqlite3.connect("./database.db")
cursor = sqlite.cursor()
cursor.execute("""

CREATE TABLE IF NOT EXISTS servers
(
 `server_id`   int NOT NULL,
 `server_name` text NOT NULL ,

PRIMARY KEY (`server_id`)
);

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

def register_server(srv : discord.server.Server):
    name = srv.name
    idd = srv.id
    getCursor().execute(f"INSERT INTO `servers` (server_id,server_name) VALUES ({idd},{name})")
    sqlite.commit()

def register_channel(chan : discord.server.Channel):
    name = chan.name
    idd = chan.id
    srvid = chan.server.id
    getCursor().execute(f"INSERT INTO `global_channels` (channel_id,channel_name,server_id) VALUES ({idd},{name},{srvid})")
    sqlite.commit()

def unregister_channel(chan : discord.server.Channel):
    idd = chan.id
    getCursor().execute(f"DELETE FROM global_channels WHERE channel_id={idd}")
    sqlite.commit()


def registered(srv : discord.server.Server):
    c = getCursor()
    c.execute(f"SELECT EXISTS(SELECT 1 FROM servers WHERE server_id={srv.id})")
    return c.fetchone()

@client.event
async def on_ready():

    print("Bot Is Online!")
    for srv in client.server:
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
    await client.say("this channel is now set as a global channel")
    channel = ctx.message.channel #here I get the channel
    register_channel(channel)
    
@client.command(pass_context=True)
async def globalstop(ctx):
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
        chanel = client.get_server(sid).get_channel(cid)
        channels.append(chanel)
    return channels

@client.event
async def on_message(message):
    if message.channel.name == "global-chat":
        if not message.author.bot:
            #channel = client.get_all_channels()
            channel = getGlobalChannels()
            for i in channel:
                if i.name == "global-chat" and i.type != discord.channel.ChannelType.private:
                    try:
                        await client.send_message(i, f"**[{message.author}@{message.server}]** `{message.content}`")
                    except discord.errors.Forbidden:
                        print(f"forbidden channel : {i.name}@{i.server.name}")

    if message.content.startswith("cookie"):
        await client.send_message(message.channel, ":cookie:")
    if message.content.startswith("thinking"):
        await client.send_message(message.channel, ":thinking:")
    if message.content.startswith("hello"):
        embed1 = discord.Embed(title="Hello :wave:", description=f"Hello {message.author.name}, How are you?",
                               color=message.author.color)
        embed1.set_thumbnail(url=message.author.avatar_url)
        embed1.set_footer(text="send by god")
        await client.send_message(message.channel, embed=embed1)
    if message.content.find(':EmojiName:'):
        for x in client.get_all_emojis():
            if x.id == '#EmojiID#':
                return await client.add_reaction(message, x)
    if message.content.startswith("help"):
        embed2 = discord.Embed(title="**Help menu**",
                               description=f"**Hello {message.author.name}, here are all comands (with prefix_):** \n"
                                           f" hi, invite, server, redriot, amiuseful, spam, invite. \n "
                                           f"**admin command:**\n ban, warn, kick",
                               color=message.author.color)
        embed2.set_thumbnail(url=message.author.avatar_url)
        embed2.set_footer(text="send by god")
        await client.send_message(message.channel, embed=embed2)
    if message.content.startswith("party"):
        await client.send_message(message.channel, ":tada:")
    if message.content.startswith("lol"):
        await client.send_message(message.channel, ":rofl:")
    if message.content.startswith("nooo"):
        await client.send_message(message.channel, ":facepalm:")
    await client.process_commands(message)


client.run("NDU2NDc4ODgyNTc3NjQ1NTY4.DryxQw.aP1IANFsvekqP8yHnvvEbaBy3wE")  # token (secret)
