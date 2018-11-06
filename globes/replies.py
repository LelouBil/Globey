import discord.ext.commands
import discord
import unicodedata
import configparser

import Globey

command = discord.ext.commands

client = Globey.client


class Replies:
    cfg = None
    reactions = {}
    embeds = {}

    replies = {}

    def __init__(self, cfg: configparser.ConfigParser):
        self.cfg = cfg
        embedscfg = list(filter(lambda n: str(n).startswith("EMBED"), cfg.sections()))
        for embd in embedscfg:
            embed = cfg[embd]
            self.embeds[embd] = self.parse_embeds(embed)
        reacts = cfg["Reactions"]
        for r in reacts:
            self.reactions[r] = unicodedata.lookup(str(reacts[r]))

        replies = cfg["Replies"]
        for r in replies:
            self.replies[r] = str(replies[r])

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        matching = [s for s in self.reactions if message.content.lower().__contains__(s)]
        for m in matching:
            await self.react(message, self.reactions[m])

        matching = [s for s in self.replies if message.content.lower().__contains__(s)]
        for m in matching:
            await client.send_message(message.channel, self.replies[m])

    async def react(self, message: discord.Message, param: str):
        await client.add_reaction(message, param)

    def is_ascii(self, s):
        return all(ord(c) < 128 for c in s)

    def is_escaped_unicode(self, str):
        # how do I determine if this is escaped unicode?
        if self.is_ascii(str):  # escaped unicode is ascii
            return True
        return False

    def parse_embeds(self, param: configparser.ConfigParser):
        aargss = {}
        for p in param:
            aargss[p] = param[p]
        e = discord.Embed(**aargss)
        return e


def setup(bot):
    config = configparser.ConfigParser()
    refile = open("reactions.ini", "r+")
    config.read_file(refile)
    refile.close()
    bot.add_cog(Replies(config))
