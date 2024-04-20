import argparse
import logging
import os
import sys
import time

import numpy as np
import pandas

from BTinterface import BTInterface
from maze import Action, Maze
from score import Scoreboard, ScoreboardFake

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

log = logging.getLogger(__name__)

# TODO : Fill in the following information
TEAM_NAME = "Team 7"
SERVER_URL = "http://140.112.175.18:5000/"
MAZE_FILE = "data/maze.csv"
BT_PORT = "/dev/tty.CAR-13"

methods = ["bfs1", "bfs2", "astar"]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="0: treasure-hunting, 1: self-testing", type=str)
    parser.add_argument("--maze-file", default=MAZE_FILE, help="Maze file", type=str)
    parser.add_argument("--bt-port", default=BT_PORT, help="Bluetooth port", type=str)
    parser.add_argument("--team-name", default=TEAM_NAME, help="Your team name", type=str)
    parser.add_argument("--server-url", default=SERVER_URL, help="Server URL", type=str)
    parser.add_argument("--method", required=True, choices=methods, help="Algorithm to run", type=str)
    return parser.parse_args()

def algorithm(_method: str, _maze: Maze):

    node_from = int(input("Enter Start Node: "))

    if _method == "bfs1":
        path = _maze.BFS(_maze.nodes[node_from - 1])

    elif _method == "bfs2":
        node_to = int(input("Enter End Node: "))
        path = _maze.BFS_2(_maze.nodes[node_from - 1], _maze.nodes[node_to - 1])

    elif _method == "astar":
        objectives = []

        for node in _maze.nodes:
            if len(node.successors) == 1:
                objectives.append(node)

        path = _maze.Astar(_maze.nodes[node_from - 1], objectives)

    actions = _maze.getActions(path)
    return _maze.actions_to_str(actions)

def main(mode: int, bt_port: str, team_name: str, server_url: str, maze_file: str, method: str):
    maze = Maze(maze_file)

    point = Scoreboard(team_name, server_url)
    # point = ScoreboardFake("your team name", "data/fakeUID.csv") # for local testing
    interface = BTInterface(port=bt_port)
    # TODO : Initialize necessary variables

    time.sleep(0.5)

    if mode == "0":

        log.info("Mode 0: For treasure-hunting")
        # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible

        interface.start()
        actionStr = algorithm(method, maze)
        actionStr += 'h'

        for i in range(len(actionStr)):
            interface.send_action(actionStr[i])

            while True:
                _uid = interface.get_UID()
                if _uid != 0:
                    if chr(int(_uid, 16)) == 'g':
                        break
                    else:
                        point.add_UID(_uid)

        interface.end_process()

    elif mode == "1":
        log.info("Mode 1: Self-testing mode.")
        # TODO: You can write your code to test specific function.

        algorithm(method, maze)

    else:
        log.error("Invalid mode")
        sys.exit(1)

if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))