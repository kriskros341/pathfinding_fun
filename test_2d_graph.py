from typing import Tuple, List, Any, TypeVar
import math

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
        def __repr__(self):
            return str(self.value)

    def __init__(self):
        super().__init__()

    def add(self, item, prio = 0):
        super().add(PrioQueue.PrioItem(item, prio))
        self.lst = sorted(self.lst, key=lambda x: x.prio, reverse=True)

    def pop(self):
        return self.lst.pop(0).value


def test_a_star():
    source = (1, 1)
    goal = (3, 3)
    tiles = [(x, y) for x in range(5) for y in range(5)]
    distances = {x: 0 for x in tiles}
    paths = {x: f"{source[0]} {source[1]}" for x in tiles}
    def pretty_format(arr: List[Tuple[Any, Any]], b: int):
        total = ""
        for i, v in enumerate(arr):
            total = f"{total} {v[0]}|{v[1]}"
            if (i+1) % b == 0:
                total = f"{total} \n"
        return total

    MOVEMENTOPTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    def apply(t1: Tuple[int, int], t2: Tuple[int, int]):
        return t1[0] + t2[0], t1[1] + t2[1]

    def cubic_distance(t1, t2):
        return math.sqrt(
                (t1[0]-t2[0])**2+
                (t1[1]-t2[1])**2
                )

    covered = [source]
    frontierQueue = PrioQueue()
    frontierQueue.add(source)

    while not frontierQueue.is_empty():
        current = frontierQueue.pop()
        covered.append(current)
        for movementOption in MOVEMENTOPTIONS:
            nextTile = apply(current, movementOption)
            if nextTile not in tiles:
                break;
            if nextTile not in covered and nextTile not in frontierQueue.lst:
                frontierQueue.add(nextTile, cubic_distance(nextTile,goal))
                distances[nextTile] = distances[current] + 1
                paths[nextTile] = \
                        f"{paths[current]} -> {nextTile[0]} {nextTile[1]}"
    print(paths[goal])


def test_flood():
    source = (1, 1)
    goal = (3, 3)
    tiles = [(x, y) for x in range(5) for y in range(5)]
    distances = {x: 0 for x in tiles}
    paths = {x: f"{source[0]} {source[1]}" for x in tiles}

    def pretty_format(arr: List[Tuple[Any, Any]], b: int):
        total = ""
        for i, v in enumerate(arr):
            total = f"{total} {v[0]}|{v[1]}"
            if (i+1) % b == 0:
                total = f"{total} \n"
        return total

    absolute_distance_map = [(abs(goal[0] - t[0]), abs(goal[1] - t[1])) for t in tiles]
    print(pretty_format(absolute_distance_map, 5))


    MOVEMENTOPTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    def apply(t1: Tuple[int, int], t2: Tuple[int, int]):
        return t1[0] + t2[0], t1[1] + t2[1]

    covered = [source]
    frontierQueue = Queue(source)
    frontierQueue.add(source)


    while not frontierQueue.is_empty():
        current = frontierQueue.pop()
        covered.append(current)
        for movementOption in MOVEMENTOPTIONS:
            nextTile = apply(current, movementOption)
            if nextTile not in tiles:
                break;
            if nextTile not in covered and nextTile not in frontierQueue.lst:
                frontierQueue.add(nextTile)
                distances[nextTile] = distances[current] + 1
                paths[nextTile] = \
                        f"{paths[current]} -> {nextTile[0]} {nextTile[1]}"
    print(paths[goal])
                
test_a_star()
test_flood()
