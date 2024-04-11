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
TEAM_NAME = "PY"
SERVER_URL = "http://140.112.175.18:5000/"
MAZE_FILE = "data/maze.csv"
BT_PORT = ""


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="0: treasure-hunting, 1: self-testing", type=str)
    parser.add_argument("--maze-file", default=MAZE_FILE, help="Maze file", type=str)
    parser.add_argument("--bt-port", default=BT_PORT, help="Bluetooth port", type=str)
    parser.add_argument(
        "--team-name", default=TEAM_NAME, help="Your team name", type=str
    )
    parser.add_argument("--server-url", default=SERVER_URL, help="Server URL", type=str)
    return parser.parse_args()


def main(mode: int, bt_port: str, team_name: str, server_url: str, maze_file: str):
    maze = Maze(maze_file)

    point = Scoreboard(team_name, server_url)
    # point = ScoreboardFake("your team name", "data/fakeUID.csv") # for local testing
    interface = BTInterface(port=bt_port)
    # TODO : Initialize necessary variables

    interface.start()

    if mode == "0":
        log.info("Mode 0: For treasure-hunting")
        # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible

        objectivesNumber = int(input("Enter Objectives Number: "))
        objectives = []

        for i in range(objectivesNumber):
            objectiveIndex = int(input(f"Enter Objective{i + 1} Index: "))
            objectives.append(maze.nodes[objectiveIndex - 1])

        node_from = int(input("Enter Start Node: "))

        path = maze.Astar(maze.nodes[node_from - 1], objectives)
        actions = maze.getActions(path)
        actionStr = maze.actions_to_str(actions)

        interface.send_action(actionStr)

    elif mode == "1":
        log.info("Mode 1: Self-testing mode.")
        # TODO: You can write your code to test specific function.

        select = input()

        if select == "BFS1":
            node_from = int(input("Enter Start Node: "))
            path = maze.BFS(maze.nodes[node_from - 1])

        elif select == "BFS2":
            node_from = int(input("Enter Start Node: "))
            node_to = int(input("Enter End Node: "))
            path = maze.BFS_2(maze.nodes[node_from - 1], maze.nodes[node_to - 1])

        elif select == "Astar":
            objectivesNumber = int(input("Enter Objectives Number: "))
            objectives = []

            for i in range(objectivesNumber):
                objectiveIndex = int(input("Enter Objective Index: "))
                objectives.append(maze.nodes[objectiveIndex - 1])

            node_from = int(input("Enter Start Node: "))

            path = maze.Astar(maze.nodes[node_from - 1], objectives)

        else:
            path = [maze.nodes[0]]

            actions = maze.getActions(path)
            maze.actions_to_str(actions)

    else:
        log.error("Invalid mode")
        sys.exit(1)

    interface.end_process()

if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))