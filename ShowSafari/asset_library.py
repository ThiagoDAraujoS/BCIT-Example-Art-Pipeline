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

    def __getitem__(self, item: UUIDString) -> Asset:
        """ Retrieve an asset from the AssetLibrary by its UUID.

        Parameters:
            item (UUIDString): The UUID (Universally Unique Identifier) of the asset to be retrieved.

        Returns:
            Asset: The asset corresponding to the provided UUID.

        Raises:
            KeyError: If the provided UUID does not exist in the AssetLibrary.

        Example usage:
            library = AssetLibrary("/path/to/asset/library")
            asset = library["12345678-1234-5678-1234-567812345678"]
        """
        item = os.path.splitext(item)[0]
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
    def remove(self, asset_uuid: UUIDString) -> None:
        """ Remove an asset from the AssetLibrary.

            This method unlinks any assets connected to the target asset and then removes the asset from the AssetLibrary.

        Parameters:
            asset_uuid (UUIDString): The UUID of the asset to be removed.

        Raises:
            AssetArchiveError: If the asset to be removed has archived assets depending on it.

        Example usage:
            library = AssetLibrary("/path/to/asset/library")
            library.remove("12345678-1234-5678-1234-567812345678")

        Note:
            Removing an asset that has archived assets depending on it will raise an AssetArchiveError.
            Archived assets cannot have their dependencies changed and must be kept for historical purposes.
        """
        if any([self[used_by].archived for used_by in self[asset_uuid].assets_used_by]):
            return ERROR(AssetArchiveError, "Cannot remove the asset while it has archived assets depending on it.")

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
    def archive(self, asset_uuid: UUIDString) -> None:
        """ Archive an asset in the AssetLibrary.

            This method creates a ZIP archive of the asset's folder, removes the asset from the AssetLibrary,
            and saves the changes.

        Parameters:
            asset_uuid (UUIDString): The UUID of the asset to be archived.

        Example usage:
            library = AssetLibrary("/path/to/asset/library")
            library.archive("12345678-1234-5678-1234-567812345678")
        """
        if self[asset_uuid].archived:
            return ERROR(AssetArchiveError, "Library can't archive an asset already archived")

        self._folder.archive_subfolder(asset_uuid)
        self[asset_uuid].archived = True

    @autosave("_save_file")
    def unpack(self, asset_uuid: UUIDString) -> None:
        """ Unpack an archived asset in the AssetLibrary.

            This method unpacks the contents of an archived asset, making it available again for use.
            The asset must have been previously archived using the `archive` method.

        Parameters:
            asset_uuid (UUIDString): The UUID of the asset to be unpacked.

        Example usage:
            library = AssetLibrary("/path/to/asset/library")
            library.unpack("12345678-1234-5678-1234-567812345678")

        Note:
            After unpacking, the asset becomes active again and can be used normally.
            Unpacking an asset that is already active will have no effect.
        """
        if not self[asset_uuid].archived:
            return ERROR(AssetArchiveError, "Library can't unpack an unarchived asset")

        self._folder.unpack_subfolder(asset_uuid)
        self[asset_uuid].archived = False

    @autosave("_save_file")
    def connect(self, parent_asset: UUIDString, child_asset: UUIDString) -> None:
        """ Connect two assets in the AssetLibrary.

            This method establishes a connection between a parent asset and a child asset by adding their UUIDs
            to each other's 'assets_used' and 'assets_used_by' attributes.

        Parameters:
            parent_asset (UUIDString): The UUID of the parent asset.
            child_asset (UUIDString): The UUID of the child asset.

        Raises:
            AssetArchiveError: If the parent asset is archived and cannot have its connections changed.
            ConnectToSelfError: If parent id and child id is the same value.

        Example usage:
            library = AssetLibrary("/path/to/asset/library")
            library.connect("12345678-1234-5678-1234-567812345678", "87654321-4321-8765-4321-876543210987")
        """
        if parent_asset == child_asset:
            return ERROR(ConnectToSelfError, "Connecting an asset to itself is not allowed.")

        if self[parent_asset].archived:
            return ERROR(AssetArchiveError, "Archived Assets can't have elements added to their 'asset_used' set")

        self[parent_asset].assets_used.add(child_asset)
        self[child_asset].assets_used_by.add(parent_asset)

    @autosave("_save_file")
    def disconnect(self, parent_asset: UUIDString, child_asset: UUIDString) -> None:
        """ Disconnect two assets in the AssetLibrary.

            This method removes the connection between a parent asset and a child asset by removing their UUIDs
            from each other's 'assets_used' and 'assets_used_by' attributes.

        Parameters:
            parent_asset (UUIDString): The UUID of the parent asset.
            child_asset (UUIDString): The UUID of the child asset.

        Raises:
            AssetArchiveError: If the parent asset is archived and cannot have its connections changed.
            ConnectToSelfError: If parent id and child id is the same value.

        Example usage:
            library = AssetLibrary("/path/to/asset/library")
            library.disconnect("12345678-1234-5678-1234-567812345678", "87654321-4321-8765-4321-876543210987")
        """
        if parent_asset == child_asset:
            return ERROR(ConnectToSelfError, "Disconnecting an asset to itself is not allowed.")

        if self[parent_asset].archived:
            return ERROR(AssetArchiveError, "Archived Assets can't have elements removed from their 'asset_used' set")

        self[parent_asset].assets_used.remove(child_asset)
        self[child_asset].assets_used_by.remove(parent_asset)

    @autosave("_save_file")
    def set_data(self, asset_id: UUIDString, asset_json: JsonString) -> None:
        """ Set data for an asset in the AssetLibrary.

            This method sets data for an asset specified by its UUID using a JSON string representation.

        Parameters:
            asset_id (UUIDString): The UUID of the asset to set data for.
            asset_json (JsonString): The JSON string representing the data to be set.

        Raises:
            AssetArchiveError: If the asset with the given UUID is archived and cannot have its data changed.

        Example usage:
            library = AssetLibrary("/path/to/asset/library")
            library.set_data("12345678-1234-5678-1234-567812345678", '{"key": "value"}')
        """
        if self[asset_id].archived:
            return ERROR(AssetArchiveError, "Cannot set data for an archived asset.")

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
