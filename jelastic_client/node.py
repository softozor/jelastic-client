from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Node:
    id: int
    int_ip: str
    node_group: str
    node_type: str
    url: str
    display_name: Optional[str] = None


Nodes = List[Node]
