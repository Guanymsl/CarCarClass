import csv
import logging
import math
from enum import IntEnum
from typing import List

import numpy as np
import pandas

from node import Direction, Node

from queue import PriorityQueue
import random

log = logging.getLogger(__name__)

class Action(IntEnum):
    ADVANCE = 1
    U_TURN = 2
    TURN_RIGHT = 3
    TURN_LEFT = 4
    HALT = 5


class Maze:
    def __init__(self, filepath: str):
        # TODO : read file and implement a data structure you like
        # For example, when parsing raw_data, you may create several Node objects.
        # Then you can store these objects into self.nodes.
        # Finally, add to nd_dict by {key(index): value(corresponding node)}

        self.raw_data = pandas.read_csv(filepath).values
        self.nodes = []
        self.node_dict = dict()  # key: index, value: the correspond node

        for _node in self.raw_data:
            self.nodes.append(Node(_node[0]))

        for _Node in self.nodes:
            _index = int(_Node.index - 1)
            for i in range(4):
                _successor = self.raw_data[_index][i + 1]
                if not math.isnan(_successor):
                    _Node.set_successor(self.nodes[int(_successor) - 1], i + 1, self.raw_data[_index][i + 5])
            self.node_dict[_index] = _Node

    def get_start_point(self):
        if len(self.node_dict) < 2:
            log.error("Error: the start point is not included.")
            return 0
        return self.node_dict[1]

    def get_node_dict(self):
        return self.node_dict

    def BFS(self, node: Node):
        # TODO : design your data structure here for your algorithm
        # Tips : return a sequence of nodes from the node to the nearest unexplored deadend

        queue = []
        visited = []
        queue.append((node , [node]))

        while queue:
            (currentNode , path) = queue.pop(0)
            cnt = 0

            visited.append(currentNode)

            for (successor, _, _) in currentNode.successors:
                if successor not in visited:
                    cnt += 1
                    queue.append((successor , path + [successor]))
                    visited.append(successor)

            if cnt == 0:
                return path

        return path

    def BFS_2(self, node_from: Node, node_to: Node):
        # TODO : similar to BFS but with fixed start point and end point
        # Tips : return a sequence of nodes of the shortest path

        queue = []
        visited = []
        queue.append((node_from , [node_from]))

        while queue:
            (currentNode , path) = queue.pop(0)

            visited.append(currentNode)

            if currentNode == node_to:
                return path

            for (successor, _, _) in currentNode.successors:
                if successor not in visited:
                    queue.append((successor, path + [successor]))
                    visited.append(successor)

        return path

    def Astar(self, node_from: Node, objectives):

        def prebfs(start):

            queue = []
            visited = []
            _distance = {}
            queue.append((start , [start]))

            while queue:
                (currentNode , path) = queue.pop(0)

                visited.append(currentNode)

                for (successor, _, _) in currentNode.successors:
                    if successor not in visited:
                        _distance[successor] = len(path)
                        queue.append((successor, path + [successor]))
                        visited.append(successor)

            _distance[start] = 0

            return _distance

        def Modify(_node, _objectives, _currentH1, _currentH2):

            maxDistance = 0

            for _objective in _objectives:
                for __objective in _objectives:
                    if distance[_objective][__objective] >= maxDistance:
                        maxDistance = distance[_objective][__objective]
                        _currentH1 = _objective
                        _currentH2 = __objective

            return (_node, _objectives, _currentH1, _currentH2)

        def Heuristic(_currentState):

            _node , _objectives , _currentH1 , _currentH2 = _currentState

            return distance[_currentH1][_currentH2] + min(distance[_currentH1][_node], distance[_currentH2][_node])

        distance = {}

        for objective in objectives:
            distance[objective] = prebfs(objective)

        initialH1 = objectives[0]
        initialH2 = objectives[0]

        if node_from in objectives:
            initialState = Modify(node_from, frozenset(objectives) - {node_from}, initialH1 , initialH2)
        else:
            initialState = Modify(node_from, frozenset(objectives), initialH1 , initialH2)

        edge = PriorityQueue()
        edge.put((0, 0, initialState))

        forwardCost = {}
        forwardCost[initialState] = 0
        backwardPath = {}
        backwardPath[initialState] = None

        while not edge.empty():

            currentCost, rand, currentState = edge.get()
            node, currentObjectives, currentH1, currentH2 = currentState

            if not currentObjectives:
                break

            for (successor, _, _) in node.successors:
                if successor in currentObjectives:
                    nextObjectives = currentObjectives - {successor}
                else:
                    nextObjectives = currentObjectives

                nextState = Modify(successor, nextObjectives, currentH1, currentH2)
                newCost = forwardCost[currentState] + 1

                if nextState not in forwardCost or newCost < forwardCost[nextState]:
                    forwardCost[nextState] = newCost
                    priority = newCost + Heuristic(nextState)
                    r = random.random()
                    edge.put((priority, r, nextState))
                    backwardPath[nextState] = currentState

        path = []

        while currentState != initialState:
            path.append(currentState[0])
            currentState = backwardPath[currentState]

        path.append(node_from)
        path.reverse()

        return path

    def getAction(self, car_dir, node_from: Node, node_to: Node):
        # TODO : get the car action
        # Tips : return an action and the next direction of the car if the node_to is the Successor of node_to
        # If not, print error message and return 0

        if node_from.is_successor(node_to):

            if car_dir == None:
                return (Action.ADVANCE, node_from.get_direction(node_to))

            nextDirection = node_from.get_direction(node_to)

            sum = car_dir + nextDirection
            dif = car_dir - nextDirection

            if dif == 0:
                action = Action.ADVANCE
            elif sum == 3 or sum == 7:
                action = Action.U_TURN
            elif dif == -3 or dif == -1 or dif == 2:
                action = Action.TURN_RIGHT
            elif dif == -2 or dif == 1 or dif == 3:
                action = Action.TURN_LEFT
            else:
                action = Action.HALT

            return (action, nextDirection)

        else:
            print(f"Node {node_to} is not a successor of {node_from}")

        return

    def getActions(self, nodes: List[Node]):
        # TODO : given a sequence of nodes, return the corresponding action sequence
        # Tips : iterate through the nodes and use getAction() in each iteration

        actions = []
        currentDirection = None

        for i in range(len(nodes) - 1):
            _action, currentDirection = self.getAction(currentDirection, nodes[i], nodes[i + 1])
            actions += [_action]

        return actions

    def actions_to_str(self, actions):
        # cmds should be a string sequence like "fbrl....", use it as the input of BFS checklist #1
        cmd = "fbrls"
        cmds = ""
        for action in actions:
            cmds += cmd[action - 1]
        log.info(cmds)
        return cmds

    def strategy(self, node: Node):
        return self.BFS(node)

    def strategy_2(self, node_from: Node, node_to: Node):
        return self.BFS_2(node_from, node_to)