from io import TextIOWrapper
from itertools import cycle

import math


def main() -> None:
    file: TextIOWrapper = open("8.txt", "rt")

    frags: list[str] = file.read().split("\n\n", 1)
    directions: str = frags[0].strip()
    nodes: list[str] = frags[1].strip().split("\n")

    node_dict: dict[str, list[str]] = {}
    starting_nodes: list[str] = []
    for node in nodes:
        new_node_name: str
        new_node_directions: list[str]
        new_node_name, new_node_directions = parse_node_string(node)

        node_dict[new_node_name] = new_node_directions
        if new_node_name.endswith("A"):
            starting_nodes.append(new_node_name)

    direction_cycle: cycle[str] = cycle(directions)

    count: int = 0
    # part 1
    # end: str = "AAA"
    # while end != "ZZZ":
    #     current_node_directions: list[str] = node_dict[end]
    #     next_direction: str = next(direction_cycle)
    #     if next_direction == "L":
    #         end = current_node_directions[0]
    #     else:
    #         end = current_node_directions[1]

    #     count += 1

    # part 2
    # it is implied heavily that these graph pathways are cyclic in nature
    # we want to keep iterating each path until it reaches a node that ends in Z

    # what if we track how long it initially takes to reach the end for each node,
    # and then how long the cycle is?
    # maybe we can find the least common multiple between these values somehow

    current_nodes: list[str] = starting_nodes.copy()
    initial_step_count: list[int] = len(starting_nodes) * [0]
    cycle_step_count: list[int] = len(starting_nodes) * [0]
    starting_cycle: set[str] = set()
    seen_cycle: set[str] = set()

    count: int = 0
    while len(seen_cycle) < len(current_nodes):
        count += 1
        next_direction: str = next(direction_cycle)
        for idx in range(len(current_nodes)):
            starting_node: str = starting_nodes[idx]
            if starting_node in seen_cycle:
                continue

            current_node: str = current_nodes[idx]
            current_node_directions: list[str] = node_dict[current_node]
            next_node: str = ""
            if next_direction == "L":
                next_node = current_node_directions[0]
            else:
                next_node = current_node_directions[1]

            current_nodes[idx] = next_node

            if next_node.endswith("Z"):
                if starting_node in starting_cycle:
                    seen_cycle.add(starting_node)
                    cycle_step_count[idx] = count - initial_step_count[idx]
                else:
                    starting_cycle.add(starting_node)
                    initial_step_count[idx] = count

    print(math.lcm(*cycle_step_count))


def parse_node_string(node_str: str) -> tuple[str, list[str]]:
    """Reads a node string and returns the node name and a list of its left and right direction node names"""
    frags: list[str] = node_str.split(" = ")
    node_name: str = frags[0]

    direction_frags: list[str] = frags[1].split(",")
    left_node_name: str = direction_frags[0].strip().strip("()")
    right_node_name: str = direction_frags[1].strip().strip("()")

    return node_name, [left_node_name, right_node_name]


if __name__ == "__main__":
    main()
