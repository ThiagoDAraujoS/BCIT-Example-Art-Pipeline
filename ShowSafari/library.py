from __future__ import annotations

from .folder import Folder
from .save_file import SaveFile, auto_save
from .data import *

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import Dict
from uuid import uuid4 as generate_uuid

ASSET_TYPES = {
    'Shot': Shot,
    'Sound': Sound,
    'Model': Model,
}


@dataclass_json
@dataclass
class LibraryData:
    data: Dict[str, Asset] = field(default_factory=dict)
    type_index: Dict[str, Set[str]] = field(default_factory=dict)


class Library:
    def __init__(self, location_path):
        self._folder: Folder = Folder(location_path, "Library")
        self._assets: LibraryData = LibraryData()
        self._save_file: SaveFile = SaveFile(self._folder, self._assets, "Library")

        self.get = self._assets.data.get
        self._save_file.load()

    @auto_save("_save_file")
    def create(self, asset_name: str, asset_type: str = "Undefined") -> str:
        """ Create a new asset and add it to the data container.

            This method creates a new asset of the specified type and adds it to the data container.
            If no asset_type is provided or the provided type is not recognized, the asset will be created
            as a generic 'Asset' type.

        Parameters:
            asset_name (str, optional): The name of the asset to be created.
            asset_type (str, optional): The type of the asset to be created.
                                        Defaults to 'Undefined' if not provided or an unrecognized type.

        Returns:
            str: A UUID (Universally Unique Identifier) representing the newly created asset.

        Example usage:
            asset_manager = Library()
            new_asset_uuid = asset_manager.create(asset_name="New Shot", asset_type="Shot")
        """
        # Prepare new asset's virtual representation
        uuid = str(generate_uuid())
        asset_type = asset_type.capitalize()
        new_asset = ASSET_TYPES.get(asset_type, Asset)(asset_name, asset_type)

        # Add asset to the data container and, type index it
        self._assets.data[uuid] = new_asset
        self._assets.type_index.setdefault(new_asset.asset_type, set()).add(uuid)

        # Setup a folder for the asset
        self._folder.setup_subfolder(uuid)
        self._folder.open_folder_in_explorer(uuid)
        return uuid

    @auto_save("_save_file")
    def remove(self, asset_uuid: str):
        # Remove the folder
        self._folder.delete_subfolder(asset_uuid)

        # Unlink any assets connected to this asset
        for used_asset in self.get(asset_uuid).assets_used:
            self.disconnect_asset(asset_uuid, used_asset)

        for used_by_asset in self.get(asset_uuid).assets_used_by:
            self.disconnect_asset(used_by_asset, asset_uuid)

        # Delete the asset from the data container
        asset = self._assets.data.pop(asset_uuid)
        if asset:
            self._assets.type_index[asset.asset_type].remove(asset_uuid)

    @auto_save("_save_file")
    def archive(self, asset_uuid: str):
        # TODO ZIP A FOLDER I MIGHT IMPLEMENT THIS ON FOLDER
        self.remove(asset_uuid)

    @auto_save("_save_file")
    def connect_asset(self, parent_asset: str, child_asset: str):
        self.get(parent_asset).assets_used.add(child_asset)
        self.get(child_asset).assets_used_by.add(parent_asset)

    @auto_save("_save_file")
    def disconnect_asset(self, parent_asset: str, child_asset: str):
        self.get(parent_asset).assets_used.remove(child_asset)
        self.get(child_asset).assets_used_by.remove(parent_asset)

    def get_by_name(self, asset_name):
        for uuid, asset in self._assets.data.items():
            if asset.name == asset_name:
                return uuid
        return None

    def get_types(self):
        return list(self._assets.type_index.keys())
