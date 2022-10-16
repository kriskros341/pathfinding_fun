from typing import Tuple

class NumericQueue():
    def __init__(self, *args):
        self.lst = []
        self.lst.extend(args)

    def is_empty(self):
        return len(self.lst) == 0
    def add(self, item):
        self.lst.append(item)           
    def pop(self):
        return self.lst.pop(0)
source = (1, 1)
goal = (4, 4)
tiles = [(x, y) for x in range(5) for y in range(5)]
distances = {x: 0 for x in tiles}
paths = {x: f"{source[0]} {source[1]}" for x in tiles}

MOVEMENTOPTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
def apply(t1: Tuple[int, int], t2: Tuple[int, int]):
    return t1[0] + t2[0], t1[1] + t2[1]

covered = [source]
frontierQueue = NumericQueue(source)
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



            

