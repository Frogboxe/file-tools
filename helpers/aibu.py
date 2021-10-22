
from tqdm import tqdm, trange

import os
from math import ceil

MEBIBYTES = 2 ** 20

def split(target: str, size: int=96) -> bool:
    if not os.path.isfile(target):
        print(f"File given not valid at path {target}")
        return False
    splits = ceil(os.path.getsize(target) / (size * MEBIBYTES))
    print(f"Reading file {target} to split into {splits} section{'s' if splits > 1 else ''}")
    with open(target, "rb") as f:
        for i in trange(splits):
            data = f.read(size * MEBIBYTES)
            with open(target + f".{str(i).rjust(4, '0')}", "wb") as w:
                w.write(data)
    return True
                
def build(pileForm: str, target: str) -> bool:
    if os.path.isfile(target):
        print(f"File target location is already occupied {target}")
        return False
    files = []
    for file in os.listdir():
        if file.startswith(pileForm) and file[-1].isdigit() and file[-2].isdigit():
            files.append(pileForm)
    with open(target, "wb") as f:
        for i in trange(len(files)):
            route = files[i]
            with open(route, "rb") as r:
                data = r.read()
            f.write(data)
    return True

