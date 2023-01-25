from enum import Enum
import json
from typing import Tuple, List, Optional, Type, TypeVar, cast, Any
import sys
import math
import string
import re
from itertools import permutations
from RomanSuite import roman_to_human

Vector3 = Tuple[int, int, int]
Edge = Tuple[Vector3, Vector3]

DEFAULT_MOVEMENT_OPTIONS = \
        [x for x in permutations((1, 0, 0))] + \
        [x for x in permutations((-1, 0, 0))]
DEFAULT_MOVEMENT_OPTIONS = [cast(Vector3, x) for x in DEFAULT_MOVEMENT_OPTIONS] 

ALPHABET = list(string.ascii_lowercase)


class Queue():
    def __init__(self, *args):
        self.lst = []
        self.lst.extend(args)
    def is_empty(self):
        return len(self.lst) == 0
    def add(self, item):
        self.lst.append(item)           
    def pop(self):
        return self.lst.pop(0)


class PrioQueue(Queue):
    class PrioItem:
        def __init__(self, value, prio):
            self.value = value
            self.prio = prio
    def __init__(self):
        super().__init__()

    def get_items(self):
        return list(map(lambda x: x.value, self.lst))

    def add(self, item, prio = 0):
        super().add(PrioQueue.PrioItem(item, prio))
        self.lst = sorted(self.lst, key=lambda x: x.prio)

    def pop(self):
        return self.lst.pop(0).value


def sum_V3(t1: Vector3, t2: Vector3) -> Vector3: 
    return t1[0] + t2[0], t1[1] + t2[1], t1[2] + t2[2]

def serialize_V3(t1: Vector3) -> str:
    return f"{t1[0]} {t1[1]} {t1[2]}"

BlockerList = List[Tuple[Vector3, Vector3]]

def pretty_format(arr: List[Tuple[Any, Any, Any]], b: int):
    total = ""
    for i, v in enumerate(arr):
        total = f"{total} {v[0]}|{v[1]}|{v[2]}"
        if (i+1) % b == 0:
            total = f"{total} \n"
    return total


def cubic_distance(t1, t2):
    return math.sqrt(
            (t1[0]-t2[0])**2+
            (t1[1]-t2[1])**2+
            (t1[2]-t2[2])**2
    )

def a_star_detailed(tiles: List[Vector3], source: Vector3, goal: Vector3,  blocked: BlockerList):
    distances = {x: 0 for x in tiles}
    paths = {x: f"{source[0]} {source[1]} {source[2]}" for x in tiles}
    covered = []
    frontierQueue = PrioQueue()
    frontierQueue.add(source)
    iteration_count = 0
    found = False
    while not frontierQueue.is_empty():
        current = frontierQueue.pop()
        covered.append(current)
        for movementOption in DEFAULT_MOVEMENT_OPTIONS:
            nextTile = sum_V3(current, movementOption)
            if nextTile not in tiles:
                continue
            if (current, nextTile) in blocked or (nextTile, current) in blocked:
                continue
            if nextTile not in covered and nextTile not in [x.value for x in frontierQueue.lst]:
                iteration_count += 1
                frontierQueue.add(nextTile, cubic_distance(nextTile,goal))
                distances[nextTile] = distances[current] + 1
                paths[nextTile] = \
                        f"{paths[current]} -> {nextTile[0]} {nextTile[1]} {nextTile[2]}"
                if nextTile == goal:
                    return paths[nextTile]
        if found:
            break
    return "Nie znaleziono drogi"

def createPath(
        boardSize: Vector3, 
        origin: Vector3, 
        destination: Vector3,
        bannedPaths: Optional[BlockerList] = None
        ):
    if not bannedPaths:
        bannedPaths = []
    tiles: List[Vector3] = [
            (x, y, z) 
            for x in range(1, boardSize[0]+1) 
            for y in range(1, boardSize[1]+1) 
            for z in range(1, boardSize[2]+1)
        ]
    path = a_star_detailed(tiles, origin, destination, bannedPaths)
    return path


def alpha_to_num(c: str):
    result = 0
    for idx, val in enumerate(c[::-1]):
        result += (ALPHABET.index(val) + 1) * len(ALPHABET) ** idx
    return result
    

def parseEncodedVertex(string: str) -> Vector3:
    re1 = r'^[I|V|X|L|C|D|M]+'
    re2 = r'^[a-z]+'
    re3 = r'^[0-9]+'
    letters_of_interest = re.search(re1, string)
    if not letters_of_interest:
        raise IOError(f"Invalid input value. Can't decode Roman numerals for: {string}")
    string = string[letters_of_interest.span(0)[1]:]
    x = roman_to_human(letters_of_interest.group(0))
    letters_of_interest = re.search(re2, string)
    if not letters_of_interest:
        raise IOError(f"Invalid input value. Can't decode a-z for: {string}")
    string = string[letters_of_interest.span(0)[1]:]
    y = alpha_to_num(letters_of_interest.group(0))
    letters_of_interest = re.search(re3, string)
    if not letters_of_interest:
        raise IOError(f"Invalid input value. Can't decode 0-9 for: {string}")
    z = int(letters_of_interest.group(0))
    return (x, y, z)

def parseBannedPaths(data: List[Tuple[str, str]]) -> List[Edge]:
    results: List[Edge] = []
    for pair in data:
        a = parseEncodedVertex(pair[0])
        b = parseEncodedVertex(pair[1])
        result: Edge = (a, b)
        results.append(result)
    return results

def main():
    #  get external arguments
    encodedOrigin = sys.argv[1]
    encodedDestination = sys.argv[2]
    if not (encodedDestination and encodedOrigin):
        raise Exception("Script missing required arguments")
    #  parse external arguments
    origin = parseEncodedVertex(encodedOrigin)
    destination = parseEncodedVertex(encodedDestination)
    bannedPaths = []
    with open("data.txt", "r") as f:
        list_of_banned_paths = [cast(Tuple[str, str], x.replace("\n", "").split(" ")) for x in f]
        bannedPaths = parseBannedPaths(list_of_banned_paths)
    bannedPaths.pop()
    bannedPaths.pop()
    bannedPaths.pop()
    config = {
        "origin": serialize_V3(origin),
        "destination": serialize_V3(destination),
        "bannedPaths": [(serialize_V3(x[0]), serialize_V3(x[1])) for x in bannedPaths]
            }
    result = createPath(
            boardSize=(5, 5, 5), 
            origin=origin, 
            destination=destination,
            bannedPaths=bannedPaths
        )

    to_write = {"final_path": result, **config}
    print(result)
    with open("result.detailed.json", "w") as f:
        f.write(json.dumps(to_write))



if __name__ == "__main__":
    main()
