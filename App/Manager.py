from __future__ import annotations
from os import path
import os
from Show import Show
from typing import Callable
from Serializable import serializable

SHOW_FILE_HEADER: str = """FILE CREATED BY: Thiago de Araujo Silva
BCIT - British Columbia Institute of Technology
Advanced Technical Arts Course
This file contains serialized show manager information."""

SHOW_FILE_NAME: str = "company"


@serializable(SHOW_FILE_HEADER, SHOW_FILE_NAME)
class Manager:
    """ The Manager class handles the management of shows and their associated files """
    def __init__(self):
        self._shows: dict[str, Show] = {}
        """ List of shows """

        self._folder_path: str = ""
        """ Path to the serialized file's folder, this is added by the serializable decorator """

    def is_installed(self) -> bool:
        return self.has_serialized_file() and self.is_serialized_file_legal()

    def install(self, folder_path: str, on_overwrite_cb: Callable[[str], None] | None = None, on_folder_collision_cb: Callable[[str], None] | None = None) -> int:
        """ Sets the main folder path for tracking show files and generate a folder to receive such files

        This method sets the main folder path to the specified `folder_path`
        for tracking show files. Optionally, you can provide callbacks to be
        executed in certain scenarios, such as when inadvertently overwriting
        a previous installation or when the new folder already exists.

        :param folder_path: The path to the main folder.
        :param on_overwrite_cb:
            A callback function to be executed when inadvertently
            overwriting a previous installation. The callback function
            should take a single argument, which is the path of the
            existing main folder. Defaults to None.
        :param on_folder_collision_cb:
            A callback function to be executed when the folder already
            exists. The callback function should take a single argument,
            which is the path of the new folder that already exists.
            Defaults to None.
        :returns: exit code 0 - installation worked fine
                  exit code 1 - couldn't install because it's already installed
                  exit code 2 - couldn't install because there is a folder in the location """
        normalized_folder_path = path.normpath(folder_path)

        if os.path.exists(normalized_folder_path):
            if self.has_serialized_file():
                if on_overwrite_cb: on_overwrite_cb(self._folder_path)
                return 1
            else:
                if on_folder_collision_cb: on_folder_collision_cb(normalized_folder_path)
                return 2

        self._folder_path = normalized_folder_path
        self.make_directory()
        self.serialize()
        return 0

    def create_show(self, name: str, on_show_folder_exists_cb: Callable[[str], None] | None = None) -> Show | None:
        """ Creates a new show with the given name

        This method creates a new instance of the Show class, sets its name
        attribute to the specified name, and returns the created show object.

        :param name: The name of the new show.
        :param on_show_folder_exists_cb:
        :return: The newly created show object or None on failure."""
        show_folder = path.normpath(path.join(self._folder_path, name))
        if path.exists(show_folder):
            if on_show_folder_exists_cb: on_show_folder_exists_cb(name)
            return None

        show: Show = Show(show_folder)
        show.name = name
        show.make_directory()
        show.serialize()
        self._shows[name] = show
        return show

    def load_shows(self) -> None:
        """ Loads shows by scanning the main folder and deserializing their metafiles

        This method populates the `shows` list with instances of the Show class
        by searching for folders within the main folder and checking for the existence
        of metafiles associated with each folder. If a metafile is found, it is deserialized
        to retrieve the show's information. """
        self._shows = {}
        for folder in os.listdir(self._folder_path):
            if path.isfile(folder):
                continue

            show_metafile = path.join(folder, Show.FILE_NAME)
            if not path.exists(show_metafile):
                continue

            show = Show.deserialize(show_metafile)
            # TODO Maybe I need to try deserialize and treat errors that if the metafile is broken
            self._shows[show.name] = show

    def print_shows(self) -> list[str]:
        """ Print the list of archived shows and return their name as a list """
        show_list = list(self._shows.keys())
        print(*show_list)
        return show_list


if __name__ == '__main__':
    FOLDER = path.normpath('C:\\Users\\Thiago\\Desktop\\Bcit Projects\\Pipeline\\Example\\CompanyName')
    manager = Manager()
    manager.install(FOLDER)
    manager.create_show("Super Raptors")
