from __future__ import annotations

from .data import *
from .folder import Folder
from .save_file import SaveFile

from uuid import UUID
from uuid import uuid4 as generate_uuid


class Library:
    """
    A class representing an asset library.
    """
    def __init__(self, folder):
        self.folder: Folder = folder
        """folder (Folder): The root folder of the library. It contains all the assets and their related subfolders."""

        self.assets: AssetDictionary = AssetDictionary()
        """assets (AssetDictionary): A dictionary of assets stored in the library, with UUID as keys and Asset objects as values. 
            This dictionary is used to keep track of all the assets in the library."""

        self.save_file: SaveFile = SaveFile(self.folder, "asset_library.json")
        """save_file (SaveFile): The file used to save and load the library's data.
            It allows the library to persist its state between sessions."""

        self.load()

    def create(self, asset_name: str = "", asset_type: str = "Undefined") -> UUID:
        """
        Creates a new asset and adds it to the library.

        Args:
            asset_name (str, optional): The name of the asset to be created. Default is an empty string.
            asset_type (str, optional): The type of the asset to be created. Default is "Undefined".

        Returns:
            UUID: The unique identifier of the created asset.

        Raises:
            None

        This method generates a new UUID for the asset and creates a subfolder in the library with the UUID as its name.
        The asset is initialized with the provided asset_name and asset_type, both of which are capitalized before use.
        If the asset_type is not recognized, it defaults to "Asset". The created asset is then added to the library's assets dictionary.

        After creating the asset and subfolder, this method opens the newly created subfolder in the file explorer.
        The library's data is then saved using the `save` method to ensure that the new asset is persisted.

        Example:
            library = Library(my_folder)
            asset_id = library.create(asset_name="My New Asset", asset_type="Texture")
            # This creates a new asset with the name "My New Asset" and type "Texture" in the library.
            # The method returns the UUID of the created asset, which can be used for further operations.
        """
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
        """
        Removes the specified asset from the library.

        Args:
            asset_uuid (UUID): The unique identifier of the asset to be removed.

        This method deletes the subfolder in the library associated with the provided asset UUID.
        After removing the asset's folder, it updates the library's assets dictionary and saves the changes using the `save` method.

        Example:
            library = Library(my_folder)
            asset_id = library.get_by_name("My Asset")
            library.remove(asset_id)
            # This removes the asset with the name "My Asset" from the library.
        """
        self.folder.delete_subfolder(str(asset_uuid))
        self.save()
        del self.assets[asset_uuid]

    def get(self, asset_uuid: UUID) -> Asset | None:
        """
        Retrieves the asset object with the specified UUID.

        Args:
            asset_uuid (UUID): The unique identifier of the asset to be retrieved.

        Returns:
            Asset | None: The asset object if found, None if not found.

        This method looks up the asset in the library's assets dictionary based on the provided UUID.
        If the asset is found, it returns the asset object; otherwise, it returns None.

        Example:
            library = Library(my_folder)
            asset_id = library.get_by_name("My Asset")
            asset_obj = library.get(asset_id)
            # This retrieves the asset object corresponding to the UUID of the asset with the name "My Asset".
        """
        return self.assets.get(asset_uuid, None)

    def get_by_name(self, asset_name: str) -> UUID | None:
        """
        Retrieves the UUID of the asset with the specified name.

        Args:
            asset_name (str): The name of the asset to be retrieved.

        Returns:
            UUID | None: The UUID of the asset if found, None if not found.

        This method iterates through the library's assets dictionary to find an asset with a matching name.
        If an asset with the specified name is found, it returns its UUID; otherwise, it returns None.

        Example:
            library = Library(my_folder)
            asset_id = library.get_by_name("My Asset")
            # This retrieves the UUID of the asset with the name "My Asset".
        """
        for uuid, asset in self.assets.items():
            if asset.name == asset_name:
                return uuid
        return None

    def save(self):
        """
        Saves the library's data to the save file.

        This method serializes the library's assets dictionary and writes it to the save file for persistence.

        Example:
            library = Library(my_folder)
            library.save()
            # This saves the library's data to the designated save file.
        """
        self.save_file.serialize(self.assets)

    def load(self):
        """
        Loads the library's data from the save file.

        This method deserializes the data from the save file and populates the library's assets dictionary with the loaded data.

        Example:
            library = Library(my_folder)
            library.load()
            # This loads the library's data from the designated save file.
        """
        loaded_library = self.save_file.deserialize(AssetDictionary)
        # TODO check if the new library reflects the folders
        self.assets = loaded_library

    def archive(self, asset_uuid: UUID):
        """
        Archives the specified asset, removing it from the library and saving the changes.

        Args:
            asset_uuid (UUID): The unique identifier of the asset to be archived.

        This method archives the asset by first removing it from the library using the `remove` method.
        After removing the asset, it saves the changes using the `save` method to ensure that the changes are persisted.

        Example:
            library = Library(my_folder)
            asset_id = library.get_by_name("My Asset")
            library.archive(asset_id)
            # This archives the asset with the name "My Asset" by removing it from the library and saving the changes.
        """
        # TODO ZIP A FOLDER I MIGHT IMPLEMENT THIS ON FOLDER
        self.remove(asset_uuid)
        self.save()

    def connect_asset(self, parent_asset: UUID, child_asset: UUID):
        """
        Connects a child asset to a parent asset.

        Args:
            parent_asset (UUID): The unique identifier of the parent asset.
            child_asset (UUID): The unique identifier of the child asset.

        This method connects a child asset to a parent asset by establishing a relationship between them.
        It utilizes the `connect` method of the parent asset to establish the connection.

        Example:
            library = Library(my_folder)
            parent_id = library.get_by_name("Parent Asset")
            child_id = library.get_by_name("Child Asset")
            library.connect_asset(parent_id, child_id)
            # This connects the asset with the name "Child Asset" as a child to the asset with the name "Parent Asset".
        """
        self.assets[parent_asset].connect(child_asset)

    def disconnect_asset(self, parent_asset: UUID, child_asset: UUID):
        """
        Disconnects a child asset from a parent asset.

        Args:
            parent_asset (UUID): The unique identifier of the parent asset.
            child_asset (UUID): The unique identifier of the child asset.

        This method disconnects a child asset from a parent asset by severing the relationship between them.
        It utilizes the `disconnect` method of the parent asset to remove the connection.

        Example:
            library = Library(my_folder)
            parent_id = library.get_by_name("Parent Asset")
            child_id = library.get_by_name("Child Asset")
            library.disconnect_asset(parent_id, child_id)
            # This disconnects the asset with the name "Child Asset" from its parent asset with the name "Parent Asset".
        """
        self.assets[parent_asset].disconnect(child_asset)
