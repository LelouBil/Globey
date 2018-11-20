import discord
import discord.ext.commands
import Globey

admins: list = []


def onload():
    adminfile = open(".admins", "r")
    for line in adminfile.readlines():
        l = line.replace("\n", "")
        if l:
            admins.append(l)


def isAdmin(id: str):
    return admins.__contains__(id)


def only_owner():
    def predicate(ctx):
        return isAdmin(ctx.message.author.id)

    return discord.ext.commands.check(predicate)