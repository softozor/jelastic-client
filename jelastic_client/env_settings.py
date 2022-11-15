from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class EnvSettings:
    displayName: Optional[str] = None
    engine: Optional[str] = None
    ishaenabled: bool = False
    region: Optional[str] = None
    shortdomain: Optional[str] = None
    sslstate: bool = False
