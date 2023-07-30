from datetime import datetime, date, time
from typing import Set, List
from dataclasses_json import dataclass_json
from dataclasses import field, dataclass


@dataclass_json
@dataclass
class Asset:
    """
    Represents a generic asset.
    """
    name: str
    _asset_type: str
    connections: List[str] = field(default_factory=list)

    @property
    def asset_type(self):
        """
        Get the type of the asset.

        Returns:
            str: The type of the asset.
        """
        return self._asset_type

    def connect(self, connection_uuid: str):
        """
        Connect the asset to another asset.

        Parameters:
            connection_uuid (str): The UUID of the asset to connect to.
        """
        self.connections.append(connection_uuid)

    def disconnect(self, connection_uuid: str):
        """
        Disconnect the asset from another asset.

        Parameters:
            connection_uuid (str): The UUID of the asset to disconnect from.
        """
        self.connections.remove(connection_uuid)


@dataclass_json
@dataclass
class Shot(Asset):
    """
    Represents a shot asset, a subclass of Asset.
    """
    clip_number: int = -1
    length: time = field(default_factory=lambda: datetime.now().time())
    characters: Set[str] = field(default_factory=set)
    environments: Set[str] = field(default_factory=set)


@dataclass_json
@dataclass
class Sound(Asset):
    """
    Represents a sound asset, a subclass of Asset.
    """
    duration: time = field(default_factory=lambda: time(0, 0, 0))
    format: str = ""
    bitrate: int = 128


@dataclass_json
@dataclass
class Model(Asset):
    """
    Represents a model asset, a subclass of Asset.
    """
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
