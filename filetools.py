
from __future__ import annotations

from typing import Callable, Union

__all__ = []

import json
import os
import shutil
import sys
from contextlib import suppress
from random import choice, randint

import pyperclip
from tqdm import tqdm

from helpers import aibu, crypt, sourceloc, filescan

GLOBAL_WIDTH = 192
GLOBAL_HEIGHT = 41

ROUTE = "\\".join(sys.argv[0].split("\\")[:-1:]) + "\\"
ROUTE_ALT = ("/".join(sys.argv[0].split("/")[:-1:]) + "/").replace("/", "\\")

ROUTE = ROUTE if len(ROUTE) > len(ROUTE_ALT) else ROUTE_ALT

exposed = set()

def expose(f: Callable) -> Callable:
    exposed.add(f.__name__)
    return f

def print_paste(string: str):
    pyperclip.copy(string)
    print(string)

def get_jumps() -> dict[str, str]:
    return json.load(open(f"{ROUTE}_jumps.json"))

def dump_jumps(d: dict[str, str]):
    json.dump(d, open(f"{ROUTE}_jumps.json", "w"))

def get_backup_style(style: str) -> dict[str, list | str]:
    return json.load(open(f"{ROUTE}\\backup-styles\\{style}"))

def get_backup_styles() -> dict[str, dict]:
    styles = {}
    for style in os.listdir(f"{ROUTE}backup-styles\\"):
        name, loaded = style.split(".")[0], get_backup_style(style)
        styles[name] = loaded
    return styles

def strenumerate(ls: list, strPad: int = 4):
    for i, terms in enumerate(ls):
        _i = str(i).rjust(strPad, " ")
        if isinstance(terms, (tuple, list)):
            yield i % GLOBAL_HEIGHT, _i, *terms
        else:
            yield i % GLOBAL_HEIGHT, _i, terms

def _summon(ln: int, defaults: list):
    args = sys.argv
    for i in range(2, ln + 2):
        try:
            y = args[i]
            yield y
        except IndexError:
            yield defaults[i - 2]

def summon(ln: int, defaults: list) -> object | list:
    if ln == 1:
        try:
            y = sys.argv[2]
            return y
        except IndexError:
            return defaults
    return list(_summon(ln, defaults))

def display(paths: list[str]):
    stringList = ["" for _ in range(GLOBAL_HEIGHT)]
    for i, _i, path in strenumerate(paths):
        slr = path.rjust(40, "-")
        stringList[i] = " | ".join((stringList[i], f"{_i} {slr}"))
    print(" ", end="")
    print("\n".join(stringList).strip())
    print("*" * GLOBAL_WIDTH)

def create_command(alias: str):
    with open(f"{ROUTE}{alias}.ps1", "w") as f:
        f.write(f"\npython \"C:\\workshop\\__ftools\\filetools.py\" {alias} $args\nC:\\workshop\\__ftools\\{alias}_.ps1\n")
    forward_command(alias, "")

def forward_command(alias: str, cmd: str):
    with open(f"{ROUTE}{alias}_.ps1", "w") as f:
        f.write(f"{cmd}")

def _l(tooltip: str, test: Callable[[str], bool], cmdName: str, cmd: str):
    cwd = os.getcwd()
    search, target = summon(2, [None, None])
    if isinstance(search, str) and search.startswith("="):
        target = search[1::]
        search = None
    print(f"{tooltip}:\n\tSearch {search}\n\tTarget: {target}")
    paths = []
    for path in os.listdir(cwd):
        if search is None and test(path):
            paths.append(path)
        elif search is not None and test(path) and search.lower() in path.lower():
            paths.append(path)
    if target is None:
        print("*" * GLOBAL_WIDTH)
        display(paths)
    else:
        print_paste(paths[int(target)])
        #forward_command(cmdName, f"{cmd} \"{cwd}\\{paths[int(target)]}\"")

def _goto(tooltip: str, cmdName: str, cmd: str, dirs: bool = False):
    target = summon(1, None)
    jumps = get_jumps()
    print(f"{tooltip}\n\tTarget: {target}")
    if target is None:
        print("*" * GLOBAL_WIDTH)
        for alias, jump in jumps.items():
            _alias, _jump = alias.rjust(20, " "), jump.ljust(20, " ")
            print(f"\t{_alias} -> {_jump}")
        print("*" * GLOBAL_WIDTH)
        return
    if not dirs:
        forward_command(cmdName, f"{cmd} \"{jumps[target]}\"")
    else:
        baseRoute = jumps[target]
        if os.path.isdir(baseRoute):
            route = baseRoute
        else:
            route = "\\".join(baseRoute.split("\\")[:-1:])
        forward_command(cmdName, f"{cmd} \"{route}\"")

def _wsn():
    cwd = os.getcwd()
    search, lim = summon(2, [None, float("inf")])
    if search is None:
        print("Need search term")
        return
    if not isinstance(lim, float):
        lim = int(lim)
    for match in filescan.wide_scan_names(cwd, search, lim):
        yield match

def _awp():
    cwd = os.getcwd()
    waypoint, filepath = summon(2, [None, None])
    if waypoint is None:
        print("Need a name for waypoint")
        return
    path = cwd if filepath is None else f"{cwd}\\{filepath}"
    jumps = get_jumps()
    jumps[waypoint] = path
    dump_jumps(jumps)

def _awd():
    waypoint = summon(1, None)
    if waypoint is None:
        print("Need a waypoint to delete")
        return
    jumps = get_jumps()
    if waypoint in jumps:
        del jumps[waypoint]
        dump_jumps(jumps)
    else:
        print("Waypoint doesn't exist!")

def _bsf():
    file = summon(1, None)
    route = f"{os.getcwd()}\\{file}"
    if file is None or not os.path.isfile(route):
        print(f"Need a file to split {route}")
        return
    aibu.split(route)

def _bbf():
    match, file = summon(2, [None, None])
    if match is None or file is None:
        print(f"Need a match and a file to reassemble binary file {match, file}")
    route = f"{os.getcwd()}\\{file}"
    aibu.build(match, route)    

def get_default_key() -> bytes:
    keyroute = "C:\\$$\\key.key"
    if os.path.isfile(keyroute):
        return open(keyroute).read()
    print(f"No default key found! Should be at {keyroute}")
    sys.exit()

@expose
def bbf():
    return _bbf()

@expose
def bsf():
    return _bsf()

@expose
def awd():
    return _awd()

@expose
def awp():
    return _awp()

@expose
def awpf():
    assert summon(2, [None, None])[1] is not None
    return _awp()

@expose
def ld():
    return _l("Directory search", os.path.isdir, "ld", "cd")

@expose
def lf():
    return _l("File search", os.path.isfile, "lf", "start")

@expose
def l():
    return _l("All search", lambda x: True, "l", "start")

@expose
def goto():
    return _goto("Goto", "goto", "cd", dirs=True)

@expose
def gotoe():
    return _goto("Goto with Explorer", "gotoe", "explorer.exe", dirs=True)

@expose
def gotol():
    return _goto("Goto and Start-Process", "gotol", "Start-Process")

@expose
def gotos():
    return _goto("Goto and 'start'", "gotos", "")

@expose
def sloc():
    sourceloc.main()

@expose
def wsn():
    for match in _wsn():
        print_paste(match)

@expose
def wsnd():
    for match in _wsn():
        if os.path.isdir(match):
            print_paste(match)

@expose
def wsnf():
    for match in _wsn():
        if os.path.isfile(match):
            print_paste(match)


@expose
def wkh():
    if os.path.isfile("key.key"):
        print("THIS WILL OVERRIDE A KEY THAT ALREADY EXISTS")
        print("THIS IS POSSIBLY VERY STUPID")
        assert input("Enter `I know and I swear I'm not a fucking idiot` to continue. Case sensitive") == "I know and I swear I'm not a fucking idiot"
        print("ok")
        with open("key.key", "rb") as keysource:
            with open(f"key.key.idiotproofing{randint(0, 100)}", "wb") as keytarget:
                keytarget.write(keysource.read())
    crypt.write_key()

@expose
def enc():
    target = summon(1, None)
    if target is None:
        print("Need file to encrypt!")
    elif not os.path.isfile(target):
        print(f"Target {target} is not a file!")
    else:
        key = get_default_key()
        crypt.encrypt(target, key)

@expose
def denc():
    target = summon(1, None)
    if target is None:
        print("Need file to decrypt!")
    elif not os.path.isfile(target):
        print(f"Target {target} is not a file!")
    else:
        key = get_default_key()
        crypt.decrypt(target, key)

@expose
def fthelp():
    with open(f"{ROUTE}readme.txt") as readme:
        print(readme.read())

@expose
def fth():
    print(exposed)

@expose
def ftset():
    attr, value = summon(2, [None, None])
    if attr is None or value is None:
        print("Need an attribute and a new value to work!")
        return
    with open(f"{ROUTE}settings.json", "r") as settingsfile:
        settings = json.load(settingsfile)
    with open(f"{ROUTE}settings.json", "w") as settingsfile:
        settings[attr] = value
        json.dump(settings, settingsfile)

@expose
def gpwd():
    attr = summon(1, None)
    if attr is None:
        print("Need an attribute to get")
    key = get_default_key()
    pdw = crypt.decrypt_json(f"{ROUTE}content.json.enc", key)
    if attr in pdw:
        print_paste(pdw[attr])
    else:
        print("Attr not found")
        se = '\n\t'.join(pdw.keys())
        print(f"Attributes: \n\t{se}")
    
@expose
def spwd():
    attr, value = summon(2, [None, None])
    if attr is None or value is None:
        print("Need an attribute and a new value to work!")
        return
    key = get_default_key()
    pdw = crypt.decrypt_json(f"{ROUTE}content.json.enc", key)
    if attr in pdw:
        print("Attribute in content already set! Delete with dpwd first")
        return
    pdw[attr] = value
    crypt.encrypt_json(f"{ROUTE}content.json.enc", key, pdw)

@expose
def dpwd():
    attr = summon(1, None)
    if attr is None:
        print("Need an attribute to delete!")
        return
    key = get_default_key()
    pdw = crypt.decrypt_json(f"{ROUTE}content.json.enc", key)
    if attr not in pdw:
        print("Attribute does not exist")
        return
    del pdw[attr]
    crypt.encrypt_json(f"{ROUTE}content.json.enc", key, pdw)

@expose
def rng():
    chars = "qwertyuiopasdfghkjzxcvbnmQWERTYUPASDDFGHJKLZXCVBNM<>,./?;:#[](){}$%^&*()1234567890"
    length = int(summon(1, 16))
    s = "".join((choice(chars) for _ in range(length)))
    print_paste(s)

@expose
def path():
    targetFile = summon(1, None)
    cwd = os.getcwd()
    if targetFile is None:
        print_paste(cwd)
        return
    target = f"{cwd}\\{targetFile}"
    if os.path.isfile(target) or os.path.isdir(target):
        print_paste(target)
    else:
        print("Invalid path!")
        print(target)


def main():
    for cmd in exposed:
        create_command(cmd)
    if len(sys.argv) == 1:
        print("No args given. Generated PowerShell Scripts (.ps1)")
        print(exposed)
        return sys.exit(1)
    if sys.argv[1] in exposed:
        globals()[sys.argv[1]]()    

if __name__ == "__main__":
    with open(f"{ROUTE}settings.json") as settingsfile:
        settings = json.load(settingsfile)
    GLOBAL_HEIGHT = int(settings["commandheight"])
    GLOBAL_WIDTH = int(settings["commandwidth"])
    main()

