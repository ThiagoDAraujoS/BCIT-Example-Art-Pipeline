from __future__ import annotations

import dataclasses
import json

from .save_file import SaveFile, autosave
from .folder import Folder
from .data import Show
from .asset_library import AssetLibrary
from . import UUIDString, JsonString, PathString, TypeString, error

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, Undefined
import os.path
from typing import Dict, Set, Callable


@dataclass_json
@dataclass
class ShowsData:
    data: Dict[str, Show] = field(default_factory=dict)
    """ Map of Show Name to Show Objects """


class ShowManager:
    FOLDER_NAME = "Shows"

    def __init__(self, main_folder_path: PathString, library_reference: AssetLibrary) -> None:
        self._main_folder_path: PathString = os.path.normpath(main_folder_path)
        """ Main folder path """

        self._folder: Folder = Folder(self._main_folder_path, ShowManager.FOLDER_NAME)
        """ Show folder representation """

        self._shows: ShowsData = ShowsData()
        """ Dictionary of Shows """

        self._save_file: SaveFile = SaveFile(self._folder, self._shows, ShowManager.FOLDER_NAME)
        """ Save file for show dictionary """

        self._library: AssetLibrary = library_reference
        """ Asset library reference """

        self._save_file.load()

    @staticmethod
    def validate_show_name(func: Callable):
        """ This decorator checks if the first argument 'show_name' exists in the _shows dictionary

            Methods decorated by this decorator need to use their first argument as a show_name id
            this id will be then checked against _shows.data and the method will be terminated or
            an error will be raised if the show_name does not exist in the _shows.data
        """
        def inner(self, show_name: str, *args, **kwargs):
            if show_name not in self._shows.data:
                return error(KeyError, "Invalid show name")
            result = func(self, show_name, *args, **kwargs)
            return result
        return inner

    @autosave("_save_file")
    def create_show(self, show_name: str) -> None:
        """ Create a new show and add it to the shows' collection.

        Parameters:
            show_name (str): The name of the new show to be created.

        Raises:
            KeyError: If a show with the same name already exists in the shows collection and IGNORE_ERRORS is False.

        Notes:
            - This method creates a new show with the specified name and adds it to the shows' collection.
            - It also sets up a subfolder for the show using the show name.

        Example usage:
            library.create_show("My Show")
        """
        if show_name in self._shows.data:
            return error(KeyError, f"Show {show_name} already presented in shows collection")

        self._shows.data[show_name] = Show()
        self._folder.setup_subfolder(show_name)

    @validate_show_name
    @autosave("_save_file")
    def delete_show(self, show_name: str) -> None:
        """ Delete a show and its associated data from the shows' collection.

        Parameters:
            show_name (str): The name of the show to be deleted.

        Raises:
            KeyError: If the specified show doesn't exist in the 'shows' collection.

        Notes:
            - This method deletes a show with the specified name from the shows' collection.
            - It also removes the associated subfolder of the show.

        Example usage:
            library.delete_show("My Show")
        """
        self._folder.delete_subfolder(show_name)
        self._shows.data.pop(show_name)

    @validate_show_name
    @autosave("_save_file")
    def set_show_data(self, show_name: str, show_json: JsonString) -> None:
        """ Set data for a show in the AssetLibrary.

        Parameters:
            show_name (str): The name of the show to set data for.
            show_json (str): The JSON string representing the data to be set.

        Example usage:
            library.set_show_data("My Show", '{"key": "value"}')
        """
        new_data = json.loads(show_json)
        for key in "shots":
            if key in new_data:
                return error(PermissionError, f"{key}, cannot be manipulated through set_data")

        loaded_instance = self[show_name].from_json(show_json)

        for dataclass_field in dataclasses.fields(self[show_name]):
            loaded_value = getattr(loaded_instance, dataclass_field.name)
            setattr(self[show_name], dataclass_field.name, loaded_value)

    @validate_show_name
    @autosave("_save_file")
    def create_shot(self, show_name: str, shot_name: str) -> UUIDString:
        """ Create a new shot and add it to a show in the AssetLibrary.

        Parameters:
            show_name (str): The name of the show to which the shot will be added.
            shot_name (str): The name of the shot to be created.

        Returns:
            UUIDString: A UUID representing the newly created shot.

        Example usage:
            new_shot_uuid = library.create_shot("My Show", "New Shot")
        """
        uuid = self._library.create(shot_name, TypeString("Shot"))
        self._shows.data[show_name].shots.append(uuid)
        return uuid

    @validate_show_name
    def get_show_data(self, show_name: str) -> JsonString:
        """ Get data for a show in the AssetLibrary.

        Parameters:
            show_name (str): The name of the show to retrieve data for.

        Returns:
            str: The JSON string representing the data for the specified show.

        Example usage:
            data = library.get_show_data("My Show")
        """
        return self._shows.data[show_name].to_json()

    @validate_show_name
    def get_show_folder(self, show_name: str) -> PathString | None:
        """ Get the folder path for a show in the AssetLibrary.

        Parameters:
            show_name (str): The name of the show to get the folder path for.

        Returns:
            PathString | None: The path to the folder for the specified show or None if the show doesn't exist.

        Example usage:
            folder_path = library.get_show_folder("My Show")
        """
        return self._folder.get_absolute_path(show_name)

    @validate_show_name
    def __getitem__(self, show_name):
        """ Get a show object from the shows' collection.

        Parameters:
            show_name (str): The name of the show to retrieve.

        Returns:
            Show: The show object for the specified show name.

        Example usage:
            show = library.get_show("My Show")
        """
        return self._shows.data[show_name]

    def get_show_names(self) -> Set[str]:
        """ Get a list of show names in the collection.

        Returns:
            Set(Show): A set containing all the show names.

        Example usage:
            show = library.get_show("My Show")
        """
        return set(self._shows.data.keys())
