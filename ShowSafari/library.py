from __future__ import annotations

from .folder import Folder
from .save_file import SaveFile
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

    def add(self, asset, uuid):
        self.data[uuid] = asset
        self.type_index.setdefault(asset.asset_type, set()).add(uuid)

    def remove(self, uuid):
        asset = self.data.pop(uuid)
        if asset:
            self.type_index[asset.asset_type].remove(uuid)


class Library:
    def __init__(self, location_path):
        self._folder: Folder = Folder(location_path, "Library")
        self._assets: LibraryData = LibraryData()
        self._save_file: SaveFile = SaveFile(self._folder, self._assets, "Library")

        self.save = self._save_file.save
        self.load = self._save_file.load
        self.get = self._assets.data.get
        self.get_by_name = self._assets.get_by_name
        self._save_file.create()
        self.load()

    def create(self, asset_name: str = "", asset_type: str = "Undefined") -> str:
        uuid = str(generate_uuid())

        asset_type = asset_type.capitalize()
        asset_name = asset_name.capitalize()

        new_asset = ASSET_TYPES.get(asset_type, Asset)(asset_name, asset_type)
        self._assets.add(new_asset, uuid)
        self._folder.create_subfolder(uuid)
        self._folder.open_folder_in_explorer(uuid)
        self.save()
        return uuid

    def remove(self, asset_uuid: str):
        self._folder.delete_subfolder(asset_uuid)
        self.save()
        self._assets.remove(asset_uuid)

    def archive(self, asset_uuid: str):
        # TODO ZIP A FOLDER I MIGHT IMPLEMENT THIS ON FOLDER
        self.remove(asset_uuid)
        self.save()

    def get_by_name(self, asset_name):
        for uuid, asset in self._assets.data.items():
            if asset.name == asset_name:
                return uuid
        return None

    def get_types(self):
        return list(self._assets.type_index.keys())

    def connect_asset(self, parent_asset: str, child_asset: str):
        self._assets.data[parent_asset].connect(child_asset)

    def disconnect_asset(self, parent_asset: str, child_asset: str):
        self._assets.data[parent_asset].disconnect(child_asset)
