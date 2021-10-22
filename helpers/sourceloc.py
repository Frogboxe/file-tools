
import os
import sys

from contextlib import suppress

NULL = "", "\n", "\r", "\n\r", "\t", "\t\t", " ", "  ", "   ", "    "

CHARS = 90
CHARSE = 110

def find_files_with_suffix(route: str, suffix: str) -> list[str]:
    routes = []
    for base, _, files in (os.walk(route)):
        for file in files:
            if file.endswith(suffix):
                routes.append(f"{base}\\{file}")
    return routes

def find_files_with_prefix(route: str, prefix: str) -> list[str]:
    routes = []
    for base, _, files in (os.walk(route)):
        for file in files:
            if file.startswith(prefix):
                routes.append(f"{base}\\{file}")
    return routes
    
def count_lines_in_file(route: str) -> int:
    with open(route, "r") as f:
        return sum((line not in NULL for line in f.readlines()))

def display_in_path_order(route: str):
    print("*" * CHARSE)
    routes = find_files_with_suffix(route, ".py")
    total = 0
    for route in routes:
        route = route.replace(".\\", "")
        token = " " * (CHARS - len(route))
        lines = count_lines_in_file(route)
        total += lines
        lstring = str(lines).rjust(6, " ")
        print(f"* {route} has{token}{lstring}")
    return total

def display_in_order(route: str, reverse: bool):
    print("*" * CHARSE)
    routes = find_files_with_suffix(route, ".py")
    total = 0
    data = {}
    for route in routes:
        data[route] = count_lines_in_file(route)
    sort = {k: v for k, v in sorted(data.items(), key=lambda item: item[1])}.items()
    if reverse:
        sort = reversed(sort); 
    for route, lines in sort:
        total += lines
        token = " " * (47 - len(route))
        lstring = str(lines).rjust(6, " ")
        print(f"* {route} has{token}{lstring}")
    return total

def main():
    startPath = "."
    sort = False
    reverse = False
    loose = False
    with suppress(IndexError):
        startPath = os.getcwd()
        reverse = sys.argv[1] == "-r"
        sort = sys.argv[1] == "-s" or reverse
        loose = sys.argv[2] == "-l"

    global NULL

    if loose:
        NULL = (NULL[0],)

    if sort:
        total = display_in_order(startPath, reverse)
    else:
        total = display_in_path_order(startPath)

    print("*" * CHARSE)
    token = (CHARS - 18) * " "
    lstring = str(total).rjust(6, " ")
    print(f"Total lines across files{token}{lstring}")
    print("*" * CHARSE)

if __name__ == "__main__":
    main()