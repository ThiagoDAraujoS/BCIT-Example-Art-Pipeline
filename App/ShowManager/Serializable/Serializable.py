import json
import os
from os import path
from enum import Enum

from .Encodable import Encodable
from .FolderManager import FolderManager

FILE_DATA_BULLET: str = "\nDATA>>>\n"


class InstallExitCode(Enum):
    SUCCESS, PATH_BROKEN, PROJECT_OVERRIDE, FOLDER_COLLISION = 0, 1, 2, 3


class Serializable(Encodable, FolderManager):
    """ Represents a class that can be serialized to a JSON file

    Inherits from:
        Encodable: Provides methods to encode and decode data from and to a JSON string.
        FolderManager: Manages a folder for storing the serialized file.
    """
    def __init__(self, folder_path: str = "", file_name: str = "", header: str = ""):
        FolderManager.__init__(self)
        if not self._folder:
            self._folder = folder_path
        self._header = header
        self._file_name = f"{file_name}.meta"

    def install(self) -> InstallExitCode:
        """ Sets the main folder path for tracking show files and generate a folder to receive such files. """
        if not os.path.exists(os.path.dirname(self._folder)):
            return InstallExitCode.PATH_BROKEN

        if os.path.exists(self._folder):
            if self.file_exists():
                return InstallExitCode.PROJECT_OVERRIDE
            else:
                return InstallExitCode.FOLDER_COLLISION

        self.create_folder()
        self.serialize()
        return InstallExitCode.SUCCESS

    def serialize(self) -> None:
        """  Serialize the object to a file. """
        file_text = self.compose_file_data()
        with open(self.get_file(), "w") as file:
            file.write(file_text)

    def deserialize(self) -> None:
        """ Deserialize the object from a file. """
        with open(self.get_file(), "r") as file:
            file_string = file.read()
        self.incorporate_file_data(file_string)

    def incorporate_file_data(self, file_string: str) -> None:
        """ Incorporate file data from into the object. """
        return self.decode(file_string.split(FILE_DATA_BULLET)[-1])

    def compose_file_data(self) -> str:
        """ Compose the file data including the header and encoded object. """
        return f"{self._header}{FILE_DATA_BULLET}{self.encode()}"

    def get_file(self) -> str:
        """ Get the full path of the serialized file. """
        return path.normpath(path.join(self._folder, self._file_name))

    def file_exists(self) -> bool:
        """ Check if the serialized file exists. """
        return path.exists(self.get_file())

    def is_installed(self) -> bool:
        return self.file_exists() and self.is_file_legal()

    def is_file_legal(self) -> bool:
        """ Check if the serialized file matches the object's structure. """
        try:
            with open(self.get_file(), "r") as file:
                file_string = file.read()
            file_string = file_string.split(FILE_DATA_BULLET)[-1]
            data = json.loads(file_string)
            type_matrix = self.__dict__
            for key, _ in data.items():
                if key not in type_matrix:
                    raise Exception("Data mismatch between python object to file text")
        except:
            return False
        return True
