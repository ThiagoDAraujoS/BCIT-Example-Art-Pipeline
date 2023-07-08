from __future__ import annotations
from os import path
import os
from enum import Enum

from .Show import Show
from .Serializable import serializable
from .SerializableDict import SerializableDict

FILE_NAME: str = "company"
FILE_HEADER: str = """FILE CREATED BY: Thiago de Araujo Silva
BCIT - British Columbia Institute of Technology
Advanced Technical Arts Course
This file contains serialized show manager information."""


class InstallExitCode(Enum):
    SUCCESS, PATH_BROKEN, PROJECT_OVERRIDE, FOLDER_COLLISION = 0, 1, 2, 3


@serializable(FILE_HEADER, FILE_NAME)
class Manager(SerializableDict):
    """ The Manager class handles the management of shows and their associated files """

    def __init__(self):
        super().__init__(Show)

    def install(self, folder_path: str) -> InstallExitCode:
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
        if not os.path.exists(os.path.dirname(normalized_folder_path)):
            return InstallExitCode.PATH_BROKEN

        if os.path.exists(normalized_folder_path):
            if self.file_exists():
                return InstallExitCode.PROJECT_OVERRIDE
            else:
                return InstallExitCode.FOLDER_COLLISION

        self._folder = normalized_folder_path
        self.create_folder()
        self.serialize()
        return InstallExitCode.SUCCESS

    def is_installed(self) -> bool:
        return self.file_exists() and self.is_file_legal()
