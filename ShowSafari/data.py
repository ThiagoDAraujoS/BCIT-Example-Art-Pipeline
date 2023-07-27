from collections import UserDict
from datetime import datetime, date, time
from typing import Set, Dict
from dataclasses_json import dataclass_json
from uuid import UUID
from dataclasses import field
from typing import List


@dataclass_json
class Asset:
    """ Represents an asset.

    Attributes:
        name (str): The name of the asset.
        connections (List[UUID]): List of UUIDs representing connections to other assets.
    """
    name: str
    connections: List[UUID] = field(default_factory=list)

    def add_connection(self, connection_uuid: UUID):
        """ add_connection(connection_uuid: UUID): Adds a connection to the asset using the provided UUID. """
        self.connections.append(connection_uuid)


@dataclass_json
class Shot(Asset):
    """ Represents a shot, a type of asset.

    Attributes:
        name (str): The name of the shot.
        connections (List[UUID]): List of UUIDs representing connections to other assets.
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
    type: str = "tv series"
    cast: Set[str] = field(default_factory=set)
    rating: int = 0
    release: date = field(default_factory=date.today)
    description: str = ""
    countries_of_origin: Set[str] = field(default_factory=set)
    third_party_services: Set[str] = field(default_factory=set)
    shots: Dict[str, Shot] = field(default_factory=dict)


@dataclass_json
class Library(UserDict):
    """ Represents a library of assets.

        Inherits from collections.UserDict.

    Attributes:
        data (dict): The dictionary containing assets with UUID keys and Asset values (default: empty dictionary).
    """
    data: dict = field(default_factory=dict)

    def __setitem__(self, key, value):
        """ __setitem__(key, value): Override of the base UserDict's __setitem__ method to enforce type constraints. """
        if not isinstance(key, UUID):
            raise TypeError(f"Keys must be of type UUID, got {type(key)} instead.")

        if not isinstance(value, Asset):
            raise TypeError(f"Values must be of type Asset, got {type(value)} instead.")

        super().__setitem__(key, value)