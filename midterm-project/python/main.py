import argparse
import logging
import sys
import time

from BTinterface import BTInterface
from maze import Maze
from score import ScoreboardServer, ScoreboardFake

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

log = logging.getLogger(__name__)

TEAM_NAME = "W3G7"
SERVER_URL = "http://140.112.175.18:5000/"
MAZE_FILE = "data/big_maze_112.csv"
BT_PORT = "/dev/tty.CAR-13"
METHOD = "astar"

methods = ["bfs1", "bfs2", "astar"]

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", help="0: treasure-hunting, 1: self-testing", type=str)
    parser.add_argument("--maze-file", default=MAZE_FILE, help="Maze file", type=str)
    parser.add_argument("--bt-port", default=BT_PORT, help="Bluetooth port", type=str)
    parser.add_argument("--team-name", default=TEAM_NAME, help="Your team name", type=str)
    parser.add_argument("--server-url", default=SERVER_URL, help="Server URL", type=str)
    parser.add_argument("--method", default=METHOD, choices=methods, help="Algorithm to run", type=str)
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

        Max = 0

        for node in _maze.nodes:
            if len(node.successors) == 1:
                objectives.append(node)
                Max = max(node.index, Max)

        path = _maze.BFS_2(_maze.nodes[node_from - 1], _maze.nodes[int(Max - 1)])
        path += _maze.Astar(_maze.nodes[int(Max - 1)], objectives)[1:]

    actions = _maze.getActions(path)
    return _maze.actions_to_str(actions)

def main(mode: int, bt_port: str, team_name: str, server_url: str, maze_file: str, method: str):
    maze = Maze(maze_file)

    interface = BTInterface(port=bt_port)
    time.sleep(0.5)

    if mode == "0":

        log.info("Mode 0: For treasure-hunting")

        interface.start()
        actionStr = algorithm(method, maze)
        actionStr += 'h'

        point = ScoreboardServer(team_name, server_url)
        # point = ScoreboardFake("your team name", "data/fakeUID.csv") # for local testing

        for i in range(len(actionStr)):
            interface.send_action(actionStr[i])
            print(f"Next action: {actionStr[i]}")

            while True:
                _uid = interface.get_UID()
                if _uid != 0:
                    if int(_uid, 16) <= 255 and chr(int(_uid, 16)) == 'g':
                        print("Arduino waiting for next action...")
                        break
                    else:
                        print(_uid)
                        if len(str.strip(_uid)[2:]) == 8 :
                            point.add_UID(str.strip(_uid)[2:])
                        else:
                            point.add_UID("0" + str.strip(_uid)[2:])
                        print(point.get_current_score())

        interface.end_process()

    elif mode == "1":
        log.info("Mode 1: Self-testing mode.")
        algorithm(method, maze)

    else:
        log.error("Invalid mode")
        sys.exit(1)

if __name__ == "__main__":
    args = parse_args()
    main(**vars(args))