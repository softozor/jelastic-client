from typing import NamedTuple, List


class Node(NamedTuple):
    id: int
    int_ip: str
    node_group: str
    node_type: str
    url: str
    display_name: str = None


Nodes = List[Node]
