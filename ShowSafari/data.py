from datetime import datetime, date, time
from typing import Set, Dict, List
from dataclasses_json import dataclass_json
from uuid import UUID
from dataclasses import field, dataclass


@dataclass_json
@dataclass
class Asset:
    """ Represents an asset.

    Attributes:
        name (str): The name of the asset.
        connections (List[str(UUID)]): List of UUIDs representing connections to other assets.
    """
    name: str
    asset_type: str
    connections: List[str] = field(default_factory=list)

    def connect(self, connection_uuid: str):
        """
        Connect the asset to another asset.

        Args:
            connection_uuid (str): The stringified UUID of the asset to connect.
        """
        self.connections.append(connection_uuid)

    def disconnect(self, connection_uuid: str):
        """
        Disconnect the asset from another asset.

        Args:
            connection_uuid (UUID): The UUID of the asset to disconnect.
        """
        self.connections.remove(connection_uuid)


@dataclass_json
@dataclass
class Shot(Asset):
    """ Represents a shot, a type of asset.

    Attributes:
        name (str): The name of the shot.
        connections (List[str(UUID)]): List of UUIDs representing connections to other assets.
        clip_number (int): The clip number of the shot (default: -1).
        length (time): The length of the shot (default: current time).
        characters (Set[str]): Set of characters in the shot (default: empty set).
        environments (Set[str]): Set of environments in the shot (default: empty set).
    """
    clip_number: int = -1
    length: time = field(default_factory=lambda: datetime.now().time())
    characters: Set[str] = field(default_factory=set)
    environments: Set[str] = field(default_factory=set)


@dataclass_json
@dataclass
class Sound(Asset):
    """ Represents a sound asset.

    Attributes:
        name (str): The name of the sound asset.
        connections (List[str(UUID)]): List of UUIDs representing connections to other assets.
        duration (float): The duration of the sound in seconds.
        format (str): The audio format of the sound (e.g., mp3, wav, etc.).
        bitrate (int): The audio bitrate in kbps.
    """
    duration: time = field(default_factory=lambda: time(0, 0, 0))
    format: str = ""
    bitrate: int = 128


@dataclass_json
@dataclass
class Model(Asset):
    """ Represents a 3D model asset.

    Attributes:
        name (str): The name of the 3D model asset.
        connections (List[str(UUID)]): List of UUIDs representing connections to other assets.
        vertices (int): The number of vertices in the model.
        faces (int): The number of faces (polygons) in the model.
    """
    vertices: int = 0
    faces: int = 0


@dataclass_json
@dataclass
class Show:
    """ Represents a TV show.

    Attributes:
        type (str): The type of the show (default: "tv series").
        cast (Set[str]): Set of cast members (default: empty set).
        rating (int): The rating of the show (default: 0).
        release (date): The release date of the show (default: current date).
        description (str): The description of the show (default: empty string).
        countries_of_origin (Set[str]): Set of countries of origin (default: empty set).
        third_party_services (Set[str]): Set of third-party services associated with the show (default: empty set).
        shots (Dict[str, Shot]): Dictionary of shots in the show, with shot names as keys (default: empty dictionary).
    """
    type: str = "Tv Series"
    cast: Set[str] = field(default_factory=set)
    rating: int = 0
    release: date = field(default_factory=date.today)
    description: str = ""
    countries_of_origin: Set[str] = field(default_factory=set)
    third_party_services: Set[str] = field(default_factory=set)
    shots: List[str] = field(default_factory=list)



