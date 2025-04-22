from enum import Enum
class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    @property
    def next(self):
        return Direction((self.value + 1) % 4)


class Ship:
    def __init__(self, x, y, d, l):
        self.location = (x, y)
        self.direction = d
        self.length = l

    @property
    def coordinate_list(self):
        x, y = self.location
        if self.direction == Direction.NORTH:
            return [(x, y - i) for i in range(self.length)]
        elif self.direction == Direction.EAST:
            return [(x + i, y) for i in range(self.length)]
        elif self.direction == Direction.SOUTH:
            return [(x, y + i) for i in range(self.length)]
        elif self.direction == Direction.WEST:
            return [(x - i, y) for i in range(self.length)]

    def rotate(self):
        self.direction = self.direction.next