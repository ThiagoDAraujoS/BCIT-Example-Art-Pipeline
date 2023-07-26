from datetime import datetime, date, time
from typing import Set, Dict
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Shot:
    clip_number: int = -1
    length: time = field(default_factory=lambda: datetime.now().time())
    characters: Set[str] = field(default_factory=set)
    environments: Set[str] = field(default_factory=set)


@dataclass_json
@dataclass
class Show:
    type: str = "tv_series"
    cast: Set[str] = field(default_factory=set)
    rating: int = 0
    release: date = field(default_factory=date.today)
    description: str = ""
    countries_of_origin: Set[str] = field(default_factory=set)
    third_party_services: Set[str] = field(default_factory=set)
    shots: Dict[str, Shot] = field(default_factory=dict)
