from datetime import date, time, datetime
from dataclasses import dataclass, field
from typing import Dict
from dataclasses_json import dataclass_json, LetterCase, Undefined


@dataclass
class Shot:
    clip_number: int = -1
    length: time = field(default_factory=lambda: datetime.now().time())
    characters: set[str] = field(default_factory=set)
    environments: set[str] = field(default_factory=set)


@dataclass_json()
@dataclass
class Show:
    type: str = "tv_series"
    cast: set[str] = field(default_factory=set)
    rating: int = 0
    release: date = field(default_factory=date.today)
    description: str = ""
    popularity_score: int = 0
    certification: dict[str, str] = field(default_factory=dict)
    countries_of_origin: set[str] = field(default_factory=set)
    third_party_services: set[str] = field(default_factory=set)
    shots: Dict[str, Shot] = field(default_factory=dict)


show = Show()
show.shots["test"] = Shot()

