from . import UUIDString, TypeString

from datetime import date, time
from typing import Set, List, Dict, Type
from dataclasses_json import dataclass_json, Undefined
from dataclasses import field, dataclass
import re


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Asset:
    """ Represents an asset.

    Attributes:
        name (str): The name of the asset.
        assets_used (Set[str(UUID)]): Set of UUIDs representing assets used by this asset.
        asset_used_by (Set[str(UUID)]): Set of UUIDs representing assets using this asset.
    """
    name: str = ""
    _asset_type: TypeString = "Undefined"
    assets_used: Set[UUIDString] = field(default_factory=set)
    asset_used_by: Set[UUIDString] = field(default_factory=set)
    archived: bool = False

    @property
    def asset_type(self) -> TypeString:
        """ Get the type of the asset. """
        return self._asset_type

    @staticmethod
    def create_asset(asset_name: str, asset_type: TypeString) -> "Asset":
        """ Factory method that generates a specialized Asset object.

            This method creates an instance of a specialized Asset object based on the provided
            asset type and name. The asset type is normalized by replacing underscores with spaces,
            capitalizing the first letter, and removing any non-alphanumeric characters at the end.
            The specialized Asset class is determined by looking up the asset type in the ASSET_TYPES
            dictionary. If the asset type is not found, a generic Asset object is created.

        Parameters:
            asset_name (str): The name of the asset.
            asset_type (str): The type of the asset.

        Returns:
            Asset: A specialized Asset object based on the provided asset type.

        Example usage:
            new_asset = Asset.create_asset("3d_model", "My Model")
            # Creates an instance of the Model class with asset type "3D Model" and name "My Model".
        """
        asset_type = asset_type.replace("_", " ").capitalize().strip()
        asset_type = re.sub(r'[^\w\s]*$', '', asset_type)
        asset_type = TypeString(asset_type)

        new_asset_type: Type = ASSET_TYPES.get(asset_type, Asset)
        return new_asset_type(asset_name, asset_type)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Shot(Asset):
    """ Represents a shot, a type of asset."""
    clip_number: int = -1
    length: time = field(default_factory=lambda: time(0, 0, 0))
    characters: Set[str] = field(default_factory=set)
    environments: Set[str] = field(default_factory=set)


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Sound(Asset):
    """ Represents a sound asset."""
    duration: time = field(default_factory=lambda: time(0, 0, 0))
    format: str = ""
    bitrate: int = 128


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Model(Asset):
    """ Represents a 3D model asset."""
    vertices: int = 0
    faces: int = 0


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass
class Show:
    """ Represents a TV show or series. """
    type: str = "Tv Series"
    cast: Set[str] = field(default_factory=set)
    rating: int = 0
    release: date = field(default_factory=date.today)
    description: str = ""
    countries_of_origin: Set[str] = field(default_factory=set)
    third_party_services: Set[str] = field(default_factory=set)
    shots: Set[str] = field(default_factory=set)


ASSET_TYPES: Dict[TypeString, Type[Asset]] = {
    TypeString(asset_type.__name__): asset_type for asset_type in Asset.__subclasses__()}
""" Dictionary containing all type names related to their type representation.
    This map allows you to pass a name ex: "Shot" and get the type Shot from it
    It automatically maps all existing variations of asset """
