from dataclasses import dataclass
from enum import Enum
from turtle import back

class Direction(Enum):
    DIR_NORTH = 0
    DIR_EAST = 1
    DIR_WEST = 2
    DIR_SOUTH = 3
    DIR_COUNT = -1

@dataclass
class Ahead:
    front: Direction
    back: Direction
    left: Direction
    right: Direction

    def set_ahead(self, ahead):
        if ahead == Direction.DIR_NORTH:
            self.front = Direction.DIR_NORTH
            self.back = Direction.DIR_SOUTH
            self.left = Direction.DIR_WEST
            self.right = Direction.DIR_EAST
        elif ahead == Direction.DIR_SOUTH:
            self.front = Direction.DIR_SOUTH
            self.back = Direction.DIR_NORTH
            self.left = Direction.DIR_EAST
            self.right = Direction.DIR_WEST
        elif ahead == Direction.DIR_EAST:
            self.front = Direction.DIR_EAST
            self.back = Direction.DIR_WEST
            self.left = Direction.DIR_NORTH
            self.right = Direction.DIR_SOUTH
        elif ahead == Direction.DIR_WEST:
            self.front = Direction.DIR_WEST
            self.back = Direction.DIR_EAST
            self.left = Direction.DIR_SOUTH
            self.right = Direction.DIR_NORTH

    def turn_left(self):
        if self.front == Direction.DIR_NORTH:
            self.set_ahead(Direction.DIR_WEST)
        elif self.front == Direction.DIR_SOUTH:
            self.set_ahead(Direction.DIR_EAST)
        elif self.front == Direction.DIR_EAST:
            self.set_ahead(Direction.DIR_NORTH)
        elif self.front == Direction.DIR_WEST:
            self.set_ahead(Direction.DIR_SOUTH)
        
    def turn_right(self):
        if self.front == Direction.DIR_NORTH:
            self.set_ahead(Direction.DIR_EAST)
        elif self.front == Direction.DIR_SOUTH:
            self.set_ahead(Direction.DIR_WEST)
        elif self.front == Direction.DIR_EAST:
            self.set_ahead(Direction.DIR_SOUTH)
        elif self.front == Direction.DIR_WEST:
            self.set_ahead(Direction.DIR_NORTH)

@dataclass
class Position:
    x: int
    y: int

    def get_pos(self):
        return self.x, self.y

    def set_pos(self, x, y):
        self.x = x
        self.y = y


class cell_msg():
    pos = Position(0, 0)

    def __init__(self, direction, x, y, block):
        self.pos.set_pos(x, y)
        self.dir = direction
        self.block = block





maze_cell = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
             [1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1],
             [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1],
             [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
             [1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
             [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
             [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
             [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
             [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1],
             [1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1],
             [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1],
             [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
             [1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1],
             [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
             [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1],
             [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 3, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]