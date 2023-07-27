from __future__ import annotations

from .data import *
from .folder import Folder
from .save_file import SaveFile

from uuid import UUID
from uuid import uuid4 as generate_uuid


class Library:
    def __init__(self, folder):
        self.folder: Folder = folder
        self.assets: AssetDictionary = AssetDictionary()
        self.save_file: SaveFile = SaveFile(self.folder, "asset_library.json")

        self.load()

    def create(self, asset_name: str = "", asset_type: str = "") -> UUID:
        uuid = generate_uuid()
        folder_name = str(uuid)

        asset_type = asset_type.capitalize()
        asset_name = asset_name.capitalize()

        self.assets[uuid] = ASSET_TYPES.get(asset_type, Asset)(asset_name, asset_type)
        self.folder.create_subfolder(folder_name)
        self.folder.open_folder_in_explorer(folder_name)
        self.save()
        return uuid

    def remove(self, asset_uuid: UUID):
        self.folder.delete_subfolder(str(asset_uuid))
        self.save()
        del self.assets[asset_uuid]

    def get(self, asset_uuid: UUID) -> Asset | None:
        return self.assets.get(asset_uuid, None)

    def get_by_name(self, asset_name: str) -> UUID | None:
        for uuid, asset in self.assets.items():
            if asset.name == asset_name:
                return uuid
        return None

    def save(self):
        self.save_file.serialize(self.assets)

    def load(self):
        loaded_library = self.save_file.deserialize(AssetDictionary)
        # TODO check if the new library reflects the folders
        self.assets = loaded_library

    def archive(self, asset_uuid: UUID):
        # TODO ZIP A FOLDER I MIGHT IMPLEMENT THIS ON FOLDER
        self.remove(asset_uuid)
        self.save()

    def connect_asset(self, parent_asset: UUID, child_asset: UUID):
        self.assets[parent_asset].connect(child_asset)

    def disconnect_asset(self, parent_asset: UUID, child_asset: UUID):
        self.assets[parent_asset].disconnect(child_asset)
