import sqlite3
import os
import discord
import Globey
import logging

log = logging.getLogger(__name__)


class GloDB:
    sqlite: sqlite3.Connection = None

    def __init__(self):
        log.info("Initializing Database")
        self.sqlite = sqlite3.connect("/storage/database.db" if not os.environ.get("GLOBEY_TEST") else "./storage"
                                                                                                       "/database.db")
        cursor = self.sqlite.cursor()
        cursor.executescript("""

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
        
        CREATE TABLE IF NOT EXISTS server_preferences(
            pref_key TEXT NOT NULL,
            pref_value TEXT NOT NULL,
            server_id integer NOT NULL,
            FOREIGN KEY(server_id) REFERENCES servers(server_id),
            PRIMARY KEY(pref_key,server_id)
        );
        """)
        log.info("Database initialized")

    def execute(self, query: str, opts: dict):
        c = self.get_cursor()
        log.debug("Executing %s", query)
        c.execute(query, opts)
        self.sqlite.commit()

    def fetch(self, query: str, opts: dict):
        c = self.get_cursor()
        c.execute(query, opts)
        log.debug("Fetching %s", query)
        self.sqlite.commit()
        return c.fetchall()

    def get_preference(self, server, key: str) -> str:

        if server is discord.Server:
            server = server.id

        log.debug("Getting preference '%s' for '%s'", key, server)
        c = self.get_cursor()
        c.execute("SELECT pref_value FROM server_preferences WHERE server_id=? AND pref_key=?", (server, key))
        res = c.fetchone()
        if res is None:
            return ""
        return res[0]

    def set_preference(self, server, key: str, value: str) -> None:
        if server is discord.Server:
            server = server.id
        log.debug("Setting preference '%s' to '%s' for '%s'", key, value, server)
        try:
            self.get_cursor().execute("INSERT INTO server_preferences (pref_key,pref_value,server_id) VALUES (?,?,?)",
                                  (str(key), str(value), str(server)))
        except sqlite3.IntegrityError as e:
            self.get_cursor().execute("UPDATE server_preferences SET pref_key=?, pref_value=?, server_id=?",
                                      (str(key), str(value), str(server)))
        self.commit()

    def get_cursor(self) -> sqlite3.Cursor:
        return self.sqlite.cursor()

    def commit(self) -> None:
        log.debug("Database commit")
        self.sqlite.commit()

    def register_server(self, srv: discord.server.Server) -> None:
        name = srv.name
        idd = srv.id
        log.debug("Registering server (%s,%s", idd, name)
        self.get_cursor().execute("INSERT INTO servers (server_id,server_name) VALUES (?,?)", (idd, name))
        self.commit()

    def delete_server(self, srv: int) -> None:
        log.debug("deleting : " + str(srv))
        self.get_cursor().execute("DELETE FROM servers WHERE server_id=" + str(srv))
        self.get_cursor().execute("DELETE FROM global_channels WHERE server_id=" + str(srv))
        self.sqlite.commit()

    def register_channel(self, chan: discord.server.Channel) -> None:
        name = chan.name
        idd = chan.id
        srvid = chan.server.id
        log.debug("Registering global channel : (%s,%s)", idd, name)
        self.get_cursor().execute(
            "INSERT INTO global_channels (channel_id,channel_name,server_id) VALUES (:id,:name,:srvid)",
            {"id": idd, "name": name, "srvid": srvid})
        self.commit()

    def unregister_channel(self, chan: discord.server.Channel) -> None:
        idd = chan.id

        self.unregister_channel_id(idd)

    def unregister_channel_id(self, id):
        log.debug("Unregistering global channel : %s", id)
        self.get_cursor().execute(f"DELETE FROM global_channels WHERE channel_id=:id", {"id": id})
        self.sqlite.commit()

    def registered(self, srv: discord.server.Server) -> bool:
        c = self.get_cursor()

        c.execute(f"SELECT EXISTS(SELECT 1 FROM servers WHERE server_id={srv.id})")
        b = c.fetchone() == (1,)
        log.debug("%s registered is ", b)
        return b

    def get_all_servers(self) -> list:
        c = self.get_cursor()
        log.debug("Getting all servers")
        c.execute("SELECT * FROM servers")
        rows = c.fetchall()
        for row in rows:
            srv = Globey.client.get_server(str(row[0]))
            if srv is None:
                log.warn(str(row[0]) + " is None")
                self.delete_server(row[0])
                continue
            yield str(row[0])

    def get_global_channels(self) -> list:
        c = self.get_cursor()
        log.debug("Getting all global channels")
        c.execute("SELECT * FROM global_channels")
        rows = c.fetchall()
        channels = list()
        for row in rows:
            cid = row[0]
            sid = row[1]
            srv = Globey.client.get_server(str(sid))
            if srv is None:
                log.warn("Server %s is None", sid)
                self.delete_server(sid)
                continue
            chanel = srv.get_channel(str(cid))
            if chanel is None:
                log.warn("Channel %s is None", cid)
                self.unregister_channel_id(cid)
                continue
            channels.append(chanel)
        return channels

    def is_global(self, channel: discord.channel.Channel) -> bool:
        c = self.get_cursor()
        c.execute(f"SELECT EXISTS(SELECT 1 FROM global_channels WHERE channel_id={channel.id})")
        b = c.fetchone() == (1,)
        log.warn("%s is_global %s", channel.id, b)
        return b
