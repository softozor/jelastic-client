from dataclasses import dataclass
from typing import Optional


@dataclass
class EnvSettings:
    displayName: Optional[str] = None
    engine: Optional[str] = None
    ishaenabled: bool = False
    region: Optional[str] = None
    shortdomain: Optional[str] = None
    sslstate: bool = False
