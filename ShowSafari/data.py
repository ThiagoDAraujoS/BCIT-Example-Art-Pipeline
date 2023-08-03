from datetime import datetime, date, time
from typing import Set, List
from dataclasses_json import dataclass_json
from dataclasses import field, dataclass


@dataclass_json
@dataclass
class Asset:
    """ Represents an asset.

    Attributes:
        name (str): The name of the asset.
        assets_used (List[str(UUID)]): List of UUIDs representing assets used by this asset.
        assets_used_by (List[str(UUID)]): List of UUIDs representing assets using this asset.
    """
    name: str
    _asset_type: str
    assets_used: Set[str] = field(default_factory=set)
    assets_used_by: Set[str] = field(default_factory=set)

    @property
    def asset_type(self):
        """
        Get the type of the asset.

        Returns:
            str: The type of the asset.
        """
        return self._asset_type


@dataclass_json
@dataclass
class Shot(Asset):
    """ Represents a shot, a type of asset."""
    clip_number: int = -1
    length: time = field(default_factory=lambda: datetime.now().time())
    characters: Set[str] = field(default_factory=set)
    environments: Set[str] = field(default_factory=set)


@dataclass_json
@dataclass
class Sound(Asset):
    """ Represents a sound asset."""
    duration: time = field(default_factory=lambda: time(0, 0, 0))
    format: str = ""
    bitrate: int = 128


@dataclass_json
@dataclass
class Model(Asset):
    """ Represents a 3D model asset."""
    vertices: int = 0
    faces: int = 0


@dataclass_json
@dataclass
class Show:
    """
    Represents a TV show or series.
    """
    type: str = "Tv Series"
    cast: Set[str] = field(default_factory=set)
    rating: int = 0
    release: date = field(default_factory=date.today)
    description: str = ""
    countries_of_origin: Set[str] = field(default_factory=set)
    third_party_services: Set[str] = field(default_factory=set)
    shots: List[str] = field(default_factory=list)
