
from __future__ import annotations

__all__ = ["wot", "silent_iter_wsn", "END_PROCESS", "HINT_STRING"]

import os
import threading
import time
from contextlib import contextmanager, suppress

from ftstripped import summon, wide_scan_names

END_PROCESS: bool = False
HINT_STRING: str = ""   # if you have lots of large files (like a bunch of long .mp4s) put the file extension
                        # name here and the script with saturate readops better on my system, it was pulling 
                        # 180 MiBs^-1 easily without so it should be fine

def silent_iter_wsn(path: str, readrand: bool = True):
    global END_PROCESS
    for path in wide_scan_names(path, "", 100_000_000):
        if os.path.isfile(path):
            with suppress(OSError):
                with open(path, "rb") as f:
                    noEOF = True
                    while not END_PROCESS and noEOF:
                        if not f.read(2 ** 16):
                            noEOF = False
        if END_PROCESS:
            return

@contextmanager
def wot(path: str, threads: int = 32):
    "Waste Of Time"
    call = lambda: silent_iter_wsn(path)
    tpool = [threading.Thread(
        target=call, 
        daemon=True)
        for _ in range(threads)]
    for thread in tpool:
        thread.start()
    try:
        yield
    finally:
        global END_PROCESS
        END_PROCESS = True
        for thread in tpool:
            thread.join()

if __name__ == "__main__":
    name, threads = summon(2, [os.getcwd(), 32])
    threads = int(threads)
    with wot(name, threads):
        while True:
            # sleeping to avoid pinning main thread unnecessarily
            time.sleep(0.04)
        

    
