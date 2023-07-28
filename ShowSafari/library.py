from __future__ import annotations

from .folder import Folder
from .save_file import SaveFile
from .data import Asset, ASSET_TYPES

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import Dict
from uuid import uuid4 as generate_uuid


@dataclass_json
@dataclass
class LibraryData:
    assets: Dict[str, Asset] = field(default_factory=dict)


class Library:
    def __init__(self, location_path):
        self._folder: Folder = Folder(location_path, "Library")
        self._data: LibraryData = LibraryData()
        self._save_file: SaveFile = SaveFile(self._folder, self._data, "Library")

        self.save = self._save_file.save
        self.load = self._save_file.load
        self.get = self._data.assets.get
        self._save_file.create()
        self.load()

    def create(self, asset_name: str = "", asset_type: str = "Undefined") -> str:
        uuid = str(generate_uuid())

        asset_type = asset_type.capitalize()
        asset_name = asset_name.capitalize()

        self._data.assets[uuid] = ASSET_TYPES.get(asset_type, Asset)(asset_name, asset_type)
        self._folder.create_subfolder(uuid)
        self._folder.open_folder_in_explorer(uuid)
        self.save()
        return uuid

    def remove(self, asset_uuid: str):
        self._folder.delete_subfolder(asset_uuid)
        self.save()
        self._data.assets.pop(asset_uuid)

    def get_by_name(self, asset_name: str) -> str | None:
        for uuid, asset in self._data.assets.items():
            if asset.name == asset_name:
                return uuid
        return None

    def archive(self, asset_uuid: str):
        # TODO ZIP A FOLDER I MIGHT IMPLEMENT THIS ON FOLDER
        self.remove(asset_uuid)
        self.save()

    def connect_asset(self, parent_asset: str, child_asset: str):
        self._data.assets[parent_asset].connect(child_asset)

    def disconnect_asset(self, parent_asset: str, child_asset: str):
        self._data.assets[parent_asset].disconnect(child_asset)
