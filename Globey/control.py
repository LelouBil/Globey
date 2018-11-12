import discord

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
