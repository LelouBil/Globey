import sqlite3
import os
import discord
import Globey
import logging
from subprocess import check_output

log = logging.getLogger(__name__)


class GloDB:
    sqlite: sqlite3.Connection = None

    def __init__(self):
        Globey.l().info("Initializing Database")

        try:
            os.remove(".temp.db")
        except FileNotFoundError:
            pass
        tmp = sqlite3.connect(".temp.db")
        cursor = tmp.cursor()
        schema_file = open("schema.sql", "r+")
        cursor.executescript(schema_file.read())
        tmp.commit()

        Globey.l().debug("Temp db initialized")

        dbfile = "/storage/database.db" if not os.environ.get("GLOBEY_TEST") else "./storage/database.db"

        cmd = f"sqldiff --transaction --schema {dbfile} .temp.db"
        result = check_output(cmd.split(" "))
        result = result.decode("utf-8")
        Globey.l().debug("SQLDIFF OUTPUT : ")
        Globey.l().debug(result)
        self.sqlite = sqlite3.connect(dbfile)
        cursor = self.sqlite.cursor()
        cursor.executescript(result)
        self.sqlite.commit()

        Globey.l().info("Database initialized")

    def execute(self, query: str, opts: dict):
        c = self.get_cursor()
        Globey.l().debug("Executing %s", query)
        c.execute(query, opts)
        self.sqlite.commit()

    def fetch(self, query: str, opts: dict):
        c = self.get_cursor()
        c.execute(query, opts)
        Globey.l().debug("Fetching %s", query)
        self.sqlite.commit()
        return c.fetchall()

    def get_preference(self, guild, key: str) -> str:

        if guild is discord.guild:
            guild = guild.id

        Globey.l().debug("Getting preference '%s' for '%s'", key, guild)
        c = self.get_cursor()
        c.execute("SELECT pref_value FROM guild_preferences WHERE guild_id=? AND pref_key=?", (str(guild), str(key)))
        res = c.fetchone()
        if res is None:
            return ""
        return res[0]

    def set_preference(self, guild, key: str, value: str) -> None:
        if isinstance(guild, discord.Guild):
            guild = guild.id
        Globey.l().debug("Setting preference '%s' to '%s' for '%s'", key, value, guild)
        try:
            self.get_cursor().execute("INSERT INTO guild_preferences (pref_key,pref_value,guild_id) VALUES (?,?,?)",
                                      (str(key), str(value), str(guild)))
        except sqlite3.IntegrityError as e:
            self.get_cursor().execute(
                "UPDATE guild_preferences SET pref_value=? WHERE main.guild_preferences.pref_key=? AND main.guild_preferences.guild_id=?",
                (str(value), str(key), str(guild)))
        self.commit()

    def get_cursor(self) -> sqlite3.Cursor:
        return self.sqlite.cursor()

    def commit(self) -> None:
        Globey.l().debug("Database commit")
        self.sqlite.commit()

    def register_guild(self, srv: discord.Guild) -> None:
        name = srv.name
        idd = srv.id
        Globey.l().debug("Registering guild (%s,%s", idd, name)
        self.get_cursor().execute("INSERT INTO guilds (guild_id,guild_name) VALUES (?,?)", (idd, name))
        self.commit()

    def delete_guild(self, srv: int) -> None:
        Globey.l().debug("deleting : " + str(srv))
        self.get_cursor().execute("DELETE FROM guilds WHERE guild_id=" + str(srv))
        self.get_cursor().execute("DELETE FROM global_channels WHERE guild_id=" + str(srv))
        self.sqlite.commit()

    def register_channel(self, chan: discord.TextChannel) -> None:
        name = chan.name
        idd = chan.id
        srvid = chan.guild.id
        Globey.l().debug("Registering global channel : (%s,%s)", idd, name)
        self.get_cursor().execute(
            "INSERT INTO global_channels (channel_id,channel_name,guild_id) VALUES (:id,:name,:srvid)",
            {"id": idd, "name": name, "srvid": srvid})
        self.commit()

    def unregister_channel(self, chan: discord.TextChannel) -> None:
        idd = chan.id

        self.unregister_channel_id(idd)

    def unregister_channel_id(self, id):
        Globey.l().debug("Unregistering global channel : %s", id)
        self.get_cursor().execute(f"DELETE FROM global_channels WHERE channel_id=:id", {"id": id})
        self.sqlite.commit()

    def registered(self, srv: discord.Guild) -> bool:
        c = self.get_cursor()

        c.execute(f"SELECT EXISTS(SELECT 1 FROM guilds WHERE guild_id={srv.id})")
        b = c.fetchone() == (1,)
        Globey.l().debug("%s registered is ", b)
        return b

    def get_all_guilds(self) -> list:
        c = self.get_cursor()
        Globey.l().debug("Getting all guilds")
        c.execute("SELECT * FROM guilds")
        rows = c.fetchall()
        for row in rows:
            srv = Globey.client.get_guild(row[0])
            if srv is None:
                Globey.l().warn(str(row[0]) + " is None")
                self.delete_guild(row[0])
                continue
            yield row[0]

    def get_global_channels(self) -> list:
        c = self.get_cursor()
        Globey.l().debug("Getting all global channels")
        c.execute("SELECT * FROM global_channels")
        rows = c.fetchall()
        channels = list()
        for row in rows:
            cid = row[0]
            sid = row[1]
            srv: discord.guild = Globey.client.get_guild(sid)
            if srv is None:
                Globey.l().warn("guild %s is None", sid)
                self.delete_guild(sid)
                continue
            chanel: discord.TextChannel = srv.get_channel(cid)
            if chanel is None:
                Globey.l().warn("Channel %s is None", cid)
                self.unregister_channel_id(cid)
                continue
            if not chanel.permissions_for(srv.get_member_named(Globey.name)).read_messages:
                Globey.l().warn("Cannot read messages from channel %s, deleting", str(chanel))
                self.unregister_channel_id(cid)
                continue
            channels.append(chanel)
        return channels

    def is_global(self, channel: discord.TextChannel) -> bool:
        c = self.get_cursor()
        c.execute(f"SELECT EXISTS(SELECT 1 FROM global_channels WHERE channel_id={channel.id})")
        b = c.fetchone() == (1,)
        Globey.l().debug("%s is_global %s", channel.id, b)
        return b
