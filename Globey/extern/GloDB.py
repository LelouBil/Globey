import sqlite3
import os
import discord
import Globey


class GloDB:
    sqlite: sqlite3.Connection = None

    def __init__(self):
        self.sqlite = sqlite3.connect("/storage/database.db" if not os.environ.get("GLOBEY_TEST") else "./database.db")
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

    def get_preference(self, server, key: str) -> str:
        if server is discord.Server:
            server = server.id

        if server is not int:
            raise TypeError

        c = self.get_cursor()
        c.execute("SELECT 1 FROM server_preferences WHERE server_id=? AND pref_key=?", {server, key})
        return c.fetchone()[1]

    def set_preference(self, server, key: str, value: str) -> None:
        if server is discord.Server:
            server = server.id

        if server is not int:
            raise TypeError
        self.get_cursor().execute("INSERT INTO server_preferences (pref_key,pref_value,server_id) VALUES (?,?,?)",
                                  {key, value, server})
        self.commit()

    def get_cursor(self) -> sqlite3.Cursor:
        return self.sqlite.cursor()

    def commit(self) -> None:
        self.sqlite.commit()

    def register_server(self, srv: discord.server.Server) -> None:
        name = srv.name
        idd = srv.id
        self.get_cursor().execute("INSERT INTO servers (server_id,server_name) VALUES (?,?)", (idd, name))
        self.commit()

    def delete_server(self, srv: int) -> None:
        print("deleting : " + str(srv))
        self.get_cursor().execute("DELETE FROM servers WHERE server_id=" + str(srv))
        self.get_cursor().execute("DELETE FROM global_channels WHERE server_id=" + str(srv))
        self.sqlite.commit()

    def register_channel(self, chan: discord.server.Channel) -> None:
        name = chan.name
        idd = chan.id
        srvid = chan.server.id
        self.get_cursor().execute(
            "INSERT INTO global_channels (channel_id,channel_name,server_id) VALUES (:id,:name,:srvid)",
            {"id": idd, "name": name, "srvid": srvid})
        self.commit()

    def unregister_channel(self, chan: discord.server.Channel) -> None:
        idd = chan.id
        self.unregister_channel_id(idd)

    def unregister_channel_id(self, id):
        self.get_cursor().execute(f"DELETE FROM global_channels WHERE channel_id=:id", {"id": id})
        self.sqlite.commit()

    def registered(self, srv: discord.server.Server) -> None:
        c = self.get_cursor()
        c.execute(f"SELECT EXISTS(SELECT 1 FROM servers WHERE server_id={srv.id})")
        return c.fetchone() == (1,)

    def get_all_servers(self) -> list:
        c = self.get_cursor()
        c.execute("SELECT * FROM servers")
        rows = c.fetchall()
        for row in rows:
            srv = Globey.client.get_server(str(row))
            if srv is None:
                self.delete_server(row[0])
            yield str(row[0])

    def get_global_channels(self) -> list:
        c = self.get_cursor()
        c.execute("SELECT * FROM global_channels")
        rows = c.fetchall()
        channels = list()
        for row in rows:
            cid = row[0]
            sid = row[1]
            srv = Globey.client.get_server(str(sid))
            if srv is None:
                self.delete_server(sid)
                self.unregister_channel_id(cid)
                continue
            chanel = srv.get_channel(str(cid))
            if chanel is None:
                self.unregister_channel_id(cid)
                continue
            channels.append(chanel)
        return channels

    def is_global(self, channel: discord.channel.Channel) -> bool:
        c = self.get_cursor()
        c.execute(f"SELECT EXISTS(SELECT 1 FROM global_channels WHERE channel_id={channel.id})")
        return c.fetchone() == (1,)
