from typing import NamedTuple


class Node(NamedTuple):
    int_ip: str
    node_group: str
    node_type: str
    display_name: str = None


Nodes = list[Node]
