
import os

def _wide_scan_names(path: str, targetString: str):
    candidates = []
    try:
        for candidate in os.listdir(path):
            paths = f"{path}\\{candidate}"
            if os.path.isfile(paths):
                if targetString in candidate:
                    yield paths
            elif os.path.isdir(paths):
                if targetString in candidate:
                    yield paths
                candidates.append(paths)
    except OSError:
        pass 
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
                        # match
                        yield candidate
                    elif isinstance(candidate, list):
                        # dirs
                        cPathsu.append(candidate)
        if li == i:
            return
        cPatha = tuple(cPathsu)

def wide_search_content_aware(path: str, targetString: str, primaryFilter: str, lim: int=1_000):
    files = wide_scan_names(path, targetString, lim)
    for file in files:
        if os.path.isfile(file):
            ...


























