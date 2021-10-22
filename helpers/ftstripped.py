from __future__ import annotations

__all__ = ["wide_search_names"]

import os
import sys
from contextlib import suppress

def _summon(ln: int, defaults: list):
    args = sys.argv
    for i in range(1, ln + 1):
        try:
            y = args[i]
            yield y
        except IndexError:
            yield defaults[i - 1]

def summon(ln: int, defaults: list):
    if ln == 1:
        try:
            y = sys.argv[2]
            return y
        except IndexError:
            return defaults
    return list(_summon(ln, defaults))

def _wide_scan_names(path: str, targetString: str):
    candidates = []
    with suppress(OSError):
        for candidate in os.listdir(path):
            paths = f"{path}\\{candidate}"
            if os.path.isfile(paths):
                if targetString in candidate:
                    yield paths
            elif os.path.isdir(paths):
                if targetString in candidate:
                    yield paths
                candidates.append(paths)
    yield candidates

def wide_scan_names(path: str, targetString: str, lim: int = 1_000):
    print(path, targetString, lim)
    i = 0
    li = -1
    cPatha = [[path]]
    while i < lim:
        cPathsu = list()
        li = i
        for cPaths in cPatha:
            for cPath in cPaths:
                for candidate in _wide_scan_names(cPath, targetString):
                    i += 1
                    if isinstance(candidate, str):
                        yield candidate
                    elif isinstance(candidate, list):
                        cPathsu.append(candidate)
        if li == i:
            return
        cPatha = tuple(cPathsu)

if __name__ == "__main__":
    print(f"Library. Don't call {__name__}")

