from typing import NamedTuple, List


class Node(NamedTuple):
    int_ip: str
    node_group: str
    node_type: str


Nodes = List[Node]
