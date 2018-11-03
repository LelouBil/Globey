#!/bin/env python3
import os.path
from subprocess import call
import argparse
import shutil

"""
glo helper script
"""

dockerpath = "/usr/bin/docker"
imagename = "globey"

tokenfile = ".glo-token"

testfile = ".test-token"
if not os.path.isfile(dockerpath):
    print("You don't have docker installed !")
    exit(1)

parser = argparse.ArgumentParser(description="Helper script to run Globey")

parser.add_argument('action', help="build, run, or brun")

parser.add_argument('-t', '--testing', help="Use the testing version", action="store_true")

args = parser.parse_args()

testing = bool(args.testing)
action = args.action


def build():
    print(f"building image {imagename}")
    current = os.getcwd()
    cmd = f"docker build -t {imagename} {current}"
    call(cmd.split(" "))
    os.remove(".token")
    print(f"building finished !")


def run():
    if not os.path.exists(os.curdir + "/storage"):
        os.mkdir(os.getcwd() + "/storage/")

    sto = os.getcwd() + "/storage/"
    cmd = f"docker run -v {sto}:/storage/ --rm -ti {imagename}"
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
if testing:
    shutil.copy2('.test-token', ".token")
    imagename += ":testing"
else:
    shutil.copy2(".glo-token", ".token")
func = switcher.get(action, noact)
print(os.getcwd())
func()
