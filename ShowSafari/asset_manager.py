from __future__ import annotations

from .data import *
from .folder import Folder

from uuid import UUID
from uuid import uuid4 as generate_uuid


class AssetManager:
    def __init__(self):
        self.folder: Folder | None = None
        """folder (Folder | None): The folder where assets will be stored. Initially set to None."""

        self.library: Library = Library()
        """library (Library): A dictionary-like object that stores the assets."""

    def get_by_name(self, asset_name: str) -> UUID | None:
        """
        Get the UUID of an asset by its name.

        Args:
            asset_name (str): The name of the asset to look for.

        Returns:
            UUID | None: The UUID of the asset if found, or None if not found.
        """
        for uuid, asset in self.library.items():
            if asset.name == asset_name:
                return uuid
        return None

    def create(self, asset_name: str = "", asset_type: str = "") -> UUID:
        """
        Create a new asset and add it to the library.

        Args:
            asset_name (str, optional): The name of the asset to create. Defaults to an empty string.
            asset_type (str, optional): The type of the asset to create. Defaults to an empty string.

        Returns:
            UUID: The UUID of the newly created asset.
        """
        uuid = generate_uuid()
        folder_name = str(uuid)

        asset_type = asset_type.capitalize()
        asset_name = asset_name.capitalize()

        self.library[uuid] = ASSET_TYPES.get(asset_type, Asset)(asset_name, asset_type)
        self.folder.create_subfolder(folder_name)
        self.folder.open_folder_in_explorer(folder_name)
        return uuid

    def remove(self, asset_uuid: UUID):
        """
        Remove an asset from the library and delete its associated folder.

        Args:
            asset_uuid (UUID): The UUID of the asset to remove.
        """
        self.folder.delete_subfolder(str(asset_uuid))
        del self.library[asset_uuid]

    def get(self, asset_uuid: UUID) -> Asset | None:
        """
        Get an asset from the library by its UUID.

        Args:
            asset_uuid (UUID): The UUID of the asset to retrieve.

        Returns:
            Asset | None: The asset object if found, or None if not found.
        """
        return self.library.get(asset_uuid, None)

    def archive(self, asset_uuid: UUID):
        """
        Archive an asset. (Method implementation is missing and should be completed).

        Args:
            asset_uuid (UUID): The UUID of the asset to archive.
        """
        pass

    def connect_asset(self, parent_asset: UUID, child_asset: UUID):
        """
        Connect a child asset to a parent asset in the library.

        Args:
            parent_asset (UUID): The UUID of the parent asset.
            child_asset (UUID): The UUID of the child asset to connect.
        """
        self.library.get(parent_asset).connect(child_asset)

    def disconnect_asset(self, parent_asset: UUID, child_asset: UUID):
        """
        Disconnect a child asset from its parent asset in the library.

        Args:
            parent_asset (UUID): The UUID of the parent asset.
            child_asset (UUID): The UUID of the child asset to disconnect.

        """
        self.library.get(parent_asset).disconnect(child_asset)
