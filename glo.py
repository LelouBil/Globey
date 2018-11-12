#!/usr/bin/env python3
import os.path
from subprocess import call
import argparse
import atexit
import shutil

"""
glo helper script
"""
dockervars = '-e GLOBEY_TOKEN='
dockerpath = "/usr/bin/docker"
windockerpath = "C:\Program Files\Docker Toolbox\docker.exe"
imagename = "globey"
contname = "globey"

tokenfile = ".glo-token"

testfile = ".test-token"
if not os.path.isfile(dockerpath) and not os.path.isfile(windockerpath):
    print("You don't have docker installed !")
    exit(1)

parser = argparse.ArgumentParser(description="Helper script to run Globey")

parser.add_argument('action', help="build, run, or brun")

parser.add_argument('-t', '--testing', help="Use the testing version", action="store_true")

args = parser.parse_args()

testing = bool(args.testing)
action = args.action


def onExit():
    cmd = f"docker rm -f {contname}"
    call(cmd.split(" "))


atexit.register(onExit)


def build():
    print(f"building image {imagename}")
    current = os.getcwd()
    cmd = f"docker build -t {imagename} {current}"
    call(cmd.split(" "))
    print(f"building finished !")


def run():
    onExit()
    if not os.path.exists(os.curdir + "/storage"):
        os.mkdir(os.getcwd() + "/storage/")

    sto = os.getcwd() + "/storage/"
    if os.name == "nt":
        print("win")
        sto = sto.replace("\\", "/")
        sto = sto.replace("C:", "/c")
    cmd = f"docker run --name {contname} -v {sto}:/storage/ {dockervars} --rm -ti {imagename}"
    print("calling : " + cmd)
    call(cmd.split(" "))


def brun():
    build()
    run()


def noact():
    print("You need to specify an action !")


switcher = {
    "build": build,
    "run": run,
    "brun": brun
}


def readToken(param):
    file = open(param, "r")
    return file.readline()


if testing:
    dockervars += readToken(".test-token")
    imagename += ":testing"
else:
    dockervars += readToken(".glo-token")
func = switcher.get(action, noact)
print(os.getcwd())
func()
