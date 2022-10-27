from typing import Generic, Tuple, List, Optional, Type, TypeVar, cast, Any
import math
import string
import re
from itertools import permutations
from RomanSuite import roman_to_human

Vector3 = Tuple[int, int, int];

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

    def add(self, item, prio = 0):
        super().add(PrioQueue.PrioItem(item, prio))
        self.lst = sorted(self.lst, key=lambda x: x.prio)

    def pop(self):
        return self.lst.pop(0).value


def sum_V3(t1: Vector3, t2: Vector3) -> Vector3: 
    return t1[0] + t2[0], t1[1] + t2[1], t1[2] + t2[2]

BlockerList = List[Tuple[Vector3, Vector3]]

def flood3d(board: List[Vector3], source: Vector3, goal: Vector3, blocked: BlockerList):
    distances = {x: 0 for x in board}
    frontierQueue = Queue(source)
    frontierQueue.add(source)
    covered = [source]
    paths = {x: f"{source[0]} {source[1]} {source[2]}" for x in board}
    iteration_count=0
    found = False
    while not frontierQueue.is_empty():
        current = frontierQueue.pop()
        covered.append(current)
        for movementOption in DEFAULT_MOVEMENT_OPTIONS:
            nextTile = sum_V3(current, movementOption)
            if nextTile not in board:
                continue;
            if (current, nextTile) in blocked or (nextTile, current) in blocked:
                continue
            if nextTile not in covered and nextTile not in frontierQueue.lst:
                iteration_count+=1
                frontierQueue.add(nextTile)
                distances[nextTile] = distances[current] + 1
                paths[nextTile] = \
                        f"{paths[current]} -> {nextTile[0]} {nextTile[1]} {nextTile[2]}"
                if nextTile == goal:
                    found = True
        if found:
            break
    print(iteration_count)
    return paths[goal]

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
def test_a_star(tiles: List[Vector3], source: Vector3, goal: Vector3,  blocked: BlockerList):
    distances = {x: 0 for x in tiles}
    paths = {x: f"{source[0]} {source[1]} {source[2]}" for x in tiles}
    
    covered = [source]
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
                continue;
            if (current, nextTile) in blocked or (nextTile, current) in blocked:
                continue
            if nextTile not in covered and nextTile not in [x.value for x in frontierQueue.lst]:
                iteration_count += 1
                frontierQueue.add(nextTile, cubic_distance(nextTile,goal))
                distances[nextTile] = distances[current] + 1
                paths[nextTile] = \
                        f"{paths[current]} -> {nextTile[0]} {nextTile[1]} {nextTile[2]}"
                if nextTile == goal:
                    found = True

        if found:
            break
    print(iteration_count)
    return paths[goal]

def createPath(boardSize: Vector3, source: Vector3, goal: Vector3, bannedPaths: Optional[BlockerList] = None):
    if not bannedPaths:
        bannedPaths = []
    tiles: List[Vector3] = [(x, y, z) for x in range(boardSize[0]) for y in range(boardSize[1]) for z in range(boardSize[2])]
    # ---------
    # flood algorithm
    path = flood3d(tiles, source, goal, bannedPaths)
    print(path)
    # A_star algorithm
    path = test_a_star(tiles, source, goal, bannedPaths)
    print(path)
    

# TODO
# Abstract board creation away
# 
# Abstract movement away

def flattened(startingList: List[Any]):
    result = []
    def helper(outerItem: Any):
        if not outerItem.__iter__ or isinstance(outerItem, str):
            result.append(outerItem)
        else:
            for innerItem in outerItem:
                helper(innerItem)
    helper(startingList)
    return result


def alpha_to_num(c: str):
    result = 0
    for idx, val in enumerate(c[::-1]):
        result += (ALPHABET.index(val) + 1) * len(ALPHABET) ** idx
    return result
    

def parseBannedPaths(data: List[str]):
    re1 = r'^[I|V|X|L|C|D|M]+'
    re2 = r'^[a-z]+'
    re3 = r'^[0-9]+'
    results = []
    for string in data:
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
        string = string[letters_of_interest.span(0)[1]:]
        z = int(letters_of_interest.group(0))

        result = sum_V3((x, y, z), (-1, -1, -1))
        results.append(result)
    return results


T = TypeVar('T')
def collect_groups_of(data: List[Any], target_length: int, as_type: Type[T] = None) -> List[T]:
    if len(data) % target_length != 0:
        raise Exception(f"Data of length {len(data)} can't be collected in groups of {target_length}")
    results = []
    for idx in range(0, len(data), target_length):
        result = data[idx:idx + target_length]
        if as_type:
            result = cast(T, tuple(result))
        results.append(result)
    return results


def main():
    with open("data.txt", "r") as f:
        l = [x.replace("\n", "").split(" ") for x in f]
        testData = []
        #testData=[((4, 4, 4), (4, 4, 3)), ((4, 4, 4), (3, 4, 4)), ((4, 4, 4), (4, 3, 4))]
        bannedPaths = collect_groups_of(
                parseBannedPaths(flattened(l)), 
                2, 
                Tuple[Vector3, Vector3]
            ) + testData
        bannedPaths.pop()
        bannedPaths.pop()
        bannedPaths.pop()
        bannedPaths.pop()
        createPath(
                boardSize=(5, 5, 5), 
                source=(0, 0, 0), 
                goal=(4, 4, 4), 
                bannedPaths=bannedPaths
            )


if __name__ == "__main__":
    main()
