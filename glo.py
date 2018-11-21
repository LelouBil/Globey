#!/usr/bin/env python3
import os.path
from subprocess import call
import argparse
import atexit
import shutil

"""
glo helper script
"""
dvars = {
    "GLOBEY_TOKEN": "",
    "GLOBEY_LOGLEVEL": "WARN"
}
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

parser.add_argument('-s', '--standalone', help="Don't use docker (not recommended)", action="store_true")

parser.add_argument('-d', '--debug', help="Set the log level to DEBUG", action="store_true")

args = parser.parse_args()

testing = bool(args.testing)
if os.path.exists(".force-test"):
    testing = True
standalone = bool(args.standalone)
debug = bool(args.debug)

if testing:
    dvars["GLOBEY_LOGLEVEL"] = "INFO"
if debug:
    dvars["GLOBEY_LOGLEVEL"] = "DEBUG"
action = args.action


def onExit():
    if standalone:
        return
    cmd = f"docker rm -f {contname}"
    call(cmd.split(" "))


atexit.register(onExit)


def build():
    if standalone:
        print("You can't do that !")
        exit(1)
    print(f"building image {imagename}")
    current = os.getcwd()
    cmd = f"docker build -t {imagename} {current}"
    call(cmd.split(" "))
    print(f"building finished !")


def get_vars():
    d = " "
    for k in dvars:
        d += f"-e {k}={dvars[k]} "
    return d


def dockerrun():
    onExit()
    if not os.path.exists(os.curdir + "/storage"):
        os.mkdir(os.getcwd() + "/storage/")

    sto = os.getcwd() + "/storage/"
    if os.name == "nt":
        print("win")
        sto = sto.replace("\\", "/")
        sto = sto.replace("C:", "/c")
    cmd = f"docker run --name {contname} -v {sto}:/storage/{get_vars()}--rm -ti {imagename}"
    print("calling : " + cmd)
    call(cmd.split(" "))


def stdrun():
    dvars["GLOBEY_TEST"] = "1"
    my_env = {**os.environ.copy(), **dvars}
    cmd = f"python3 -m Globey"
    call(cmd.split(" "), env=my_env)


def run():
    if standalone:
        stdrun()
    else:
        dockerrun()


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
    dvars["GLOBEY_TOKEN"] = readToken(".test-token")
    imagename += ":testing"
else:
    dvars["GLOBEY_TOKEN"] = readToken(".glo-token")
func = switcher.get(action, noact)
print(os.getcwd())
func()
