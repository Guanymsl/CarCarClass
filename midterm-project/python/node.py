from enum import IntEnum

class Direction(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

class Node:
    def __init__(self, index: int = 0):
        self.index = index
        self.successors = []

    def get_index(self):
        return self.index

    def get_successors(self):
        return self.successors

    def set_successor(self, successor, direction, length=1):
        self.successors.append((successor, Direction(direction), int(length)))
        print(f"For Node {self.index}, a successor {self.successors[-1]} is set.")
        return

    def get_direction(self, node):
        for _successor in self.successors:
            if _successor[0] == node:
                return _successor[1]

        print(f"Node {node} is not a successor of {self.index}")
        return

    def is_successor(self, node):
        for succ in self.successors:
            if succ[0] == node:
                return True
        return False