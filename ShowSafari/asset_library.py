from __future__ import annotations

import os

from .folder import Folder
from .save_file import SaveFile, autosave
from .data import *
from . import UUIDString, JsonString, PathString, TypeString
from . import AssetArchiveError, ConnectToSelfError, ERROR

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, Undefined
from typing import Dict
from uuid import uuid4 as generate_uuid


@dataclass_json
@dataclass
class LibraryData:
    data: Dict[UUIDString, Asset] = field(default_factory=dict)
    """ All Asset data is contained in this dictionary of UUIDs:Assets """

    type_index: Dict[TypeString, Set[UUIDString]] = field(default_factory=dict)
    """ This is tagged Object data structure. It records asset type groups, 
        each group contain a set of asset UUIDS of a given type """


class AssetLibrary:
    FOLDER_NAME = "Library"

    def __init__(self, location_path: PathString) -> None:
        """ Initialize an AssetLibrary object.

        Parameters:
            location_path (PathString):
                The location path where the AssetLibrary will be initialized.

        Notes:
            - This method initializes an AssetLibrary object by creating a folder and loading existing assets' data.

        Example usage:
            library = AssetLibrary("/path/to/asset/library")
        """
        self._folder: Folder = Folder(location_path, AssetLibrary.FOLDER_NAME)
        self._assets: LibraryData = LibraryData()
        self._save_file: SaveFile = SaveFile(self._folder, self._assets, AssetLibrary.FOLDER_NAME)
        self._save_file.load()

    def __getitem__(self, item: str):
        """ This method receives a UUID and return an asset contained in the Library """
        return self._assets.data[item]

    @autosave("_save_file")
    def create(self, asset_name: str, asset_type: TypeString = "Undefined") -> UUIDString:
        """ Create a new asset and add it to the AssetLibrary.

            This method creates a new asset of the specified type and adds it to the AssetLibrary's data container.
            If no asset_type is provided or the provided type is not recognized,
            the asset will be created as a generic 'Asset' type.

        Parameters:
            asset_name (str): The name of the asset to be created.
            asset_type (str, optional): The type of the asset to be created.
                                        Defaults to 'Undefined' if not provided or an unrecognized type.

        Returns:
            UUIDString: A UUID string representing the newly created asset.

        Example usage:
            library = AssetLibrary("/path/to/asset/library")
            new_asset_uuid = library.create(asset_name="New Shot", asset_type="Shot")
        """
        # Prepare new asset's virtual representation
        uuid = UUIDString(str(generate_uuid()))
        new_asset = Asset.create_asset(asset_name, asset_type)

        # Add asset to the data container and, type index it
        self._assets.data[uuid] = new_asset
        self._assets.type_index.setdefault(new_asset.asset_type, set()).add(uuid)

        # Setup a folder for the asset
        self._folder.setup_subfolder(uuid)
        self._folder.open_folder_in_explorer(uuid)
        return UUIDString(uuid)

    @autosave("_save_file")
    def remove(self, asset_uuid: str):
        # Unlink any assets connected to this asset
        for used_asset in self[asset_uuid].assets_used:
            self.disconnect(asset_uuid, used_asset)

        for used_by_asset in self[asset_uuid].assets_used_by:
            self.disconnect(used_by_asset, asset_uuid)

        # Remove the folder
        self._folder.delete_subfolder(asset_uuid)

        # Delete the asset from the data container
        asset = self._assets.data.pop(asset_uuid)
        if asset:
            self._assets.type_index[asset.asset_type].remove(asset_uuid)

    @autosave("_save_file")
    def archive(self, asset_uuid: str):
        # TODO ZIP A FOLDER I MIGHT IMPLEMENT THIS ON FOLDER
        self.remove(asset_uuid)

    @autosave("_save_file")
    def connect(self, parent_asset: str, child_asset: str):
        print(self._assets.data)
        self[parent_asset].assets_used.add(child_asset)
        self[child_asset].assets_used_by.add(parent_asset)

    @autosave("_save_file")
    def disconnect(self, parent_asset: str, child_asset: str):
        self[parent_asset].assets_used.remove(child_asset)
        self[child_asset].assets_used_by.remove(parent_asset)

    @autosave("_save_file")
    def set_data(self, asset_id: str, asset_json: str):
        self[asset_id].from_json(asset_json, undefine=Undefined.EXCLUDE)

    def get_data(self, asset_id: UUIDString) -> JsonString:
        """ Get data for an asset in the AssetLibrary.

            This method retrieves data for an asset specified by its UUID and returns it as a JSON string representation.

        Parameters:
            asset_id (UUIDString): The UUID of the asset to retrieve data for.

        Returns:
            JsonString: The JSON string representing the data for the specified asset.

        Example usage:
            library = AssetLibrary("/path/to/asset/library")
            data = library.get_data("12345678-1234-5678-1234-567812345678")
        """
        return self[asset_id].to_json()

    def get_by_name(self, asset_name: str) -> Set[UUIDString]:
        """ Get the UUID of an asset by its name in the AssetLibrary.

            This method searches for assets with the provided name and returns a set of UUIDs if found.

        Parameters:
            asset_name (str): The name of the asset to find.

        Returns:
            Set[UUIDString]: A set containing the UUIDs of assets with the specified name, or an empty set if not found.

        Example usage:
            library = AssetLibrary("/path/to/asset/library")
            asset_uuids = library.get_by_name("MyAsset")
        """
        return {uuid for uuid, asset in self._assets.data.items() if asset.name == asset_name}

    def get_types(self) -> Set[TypeString]:
        """ Get all asset types available in the AssetLibrary.

            This method returns a set containing all unique asset types present in the AssetLibrary.

        Returns:
            Set[TypeString]: A set of all unique asset types in the AssetLibrary.

        Example usage:
            library = AssetLibrary("/path/to/asset/library")
            asset_types = library.get_types()
        """
        return set(self._assets.type_index.keys())

    def get_all_assets(self) -> Set[UUIDString]:
        """ Get all assets' UUIDs in the AssetLibrary.

            This method returns a set containing all UUIDs of assets present in the AssetLibrary.

        Returns:
            Set[UUIDString]: A set of all asset UUIDs in the AssetLibrary.

        Example usage:
            library = AssetLibrary("/path/to/asset/library")
            all_asset_uuids = library.get_all_assets()
        """
        return set(self._assets.data.keys())

    def get_all_assets_of_type(self, asset_type: TypeString) -> Set[UUIDString]:
        """ Get all assets' UUIDs of a specific type in the AssetLibrary.

            This method returns a set containing all UUIDs of assets of the specified type present in the AssetLibrary.

        Parameters:
            asset_type (TypeString): The type of assets to retrieve.

        Returns:
            Set[UUIDString]: A set of all asset UUIDs of the specified type in the AssetLibrary.

        Example usage:
            library = AssetLibrary("/path/to/asset/library")
            assets_of_type = library.get_all_assets_of_type("Shot")
        """
        return self._assets.type_index.get(asset_type, set())
