from __future__ import annotations
from ShowSafari import *
from typing import Dict
from uuid import uuid4 as generate_uuid


class Library:
    def __init__(self, location_path):
        self.folder: Folder = Folder(location_path, "Library")
        self.assets: Dict[str, Asset] = {}
        self.save_file: SaveFile = SaveFile(self.folder, dict, "asset_library.json")
        self.load()

    def create(self, asset_name: str = "", asset_type: str = "Undefined") -> str:
        uuid = str(generate_uuid())

        asset_type = asset_type.capitalize()
        asset_name = asset_name.capitalize()

        self.assets[uuid] = ASSET_TYPES.get(asset_type, Asset)(asset_name, asset_type)
        self.folder.create_subfolder(uuid)
        self.folder.open_folder_in_explorer(uuid)
        self.save()
        return uuid

    def remove(self, asset_uuid: str):
        self.folder.delete_subfolder(asset_uuid)
        self.save()
        del self.assets[asset_uuid]

    def get(self, asset_uuid: str) -> Asset | None:
        return self.assets.get(asset_uuid, None)

    def get_by_name(self, asset_name: str) -> str | None:
        for uuid, asset in self.assets.items():
            if asset.name == asset_name:
                return uuid
        return None

    def save(self):
        self.save_file.serialize(self.assets)

    def load(self):
        loaded_library = self.save_file.deserialize()
        # TODO check if the new library reflects the folders
        self.assets = loaded_library

    def archive(self, asset_uuid: str):
        # TODO ZIP A FOLDER I MIGHT IMPLEMENT THIS ON FOLDER
        self.remove(asset_uuid)
        self.save()

    def connect_asset(self, parent_asset: str, child_asset: str):
        self.assets[parent_asset].connect(child_asset)

    def disconnect_asset(self, parent_asset: str, child_asset: str):
        self.assets[parent_asset].disconnect(child_asset)
