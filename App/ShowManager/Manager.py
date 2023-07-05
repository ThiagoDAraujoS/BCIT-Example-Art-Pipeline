from __future__ import annotations
from typing import Callable

from os import path
import os

from .Show import Show
from .Serializable import serializable
from .SerializableDict import SerializableDict

FILE_NAME: str = "company"
FILE_HEADER: str = """FILE CREATED BY: Thiago de Araujo Silva
BCIT - British Columbia Institute of Technology
Advanced Technical Arts Course
This file contains serialized show manager information."""


@serializable(FILE_HEADER, FILE_NAME)
class Manager(SerializableDict):
    """ The Manager class handles the management of shows and their associated files """

    def __init__(self):
        super().__init__(Show)

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
                if on_overwrite_cb:
                    on_overwrite_cb(self._folder_path)
                return 1
            else:
                if on_folder_collision_cb:
                    on_folder_collision_cb(normalized_folder_path)
                return 2

        self._folder_path = normalized_folder_path
        self.make_directory()
        self.serialize()
        return 0

    def is_installed(self) -> bool:
        return self.has_serialized_file() and self.is_serialized_file_legal()
