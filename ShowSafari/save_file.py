from ShowSafari import *
import os.path
from typing import Type
from dataclasses_json import dataclass_json


class SaveFile:
    """
    A class representing a save file for serializing and deserializing data.

    Attributes:
        _folder (Folder): The folder in which the save file is located.
        _file_path (str): The full path to the save file.

    Methods:
        __init__(self, folder: Folder, file_name: str)
            Initializes the SaveFile with a specified folder and file name.

        serialize(self, data_content: dataclass_json) -> None
            Serializes the given data_content and writes it to the save file.

        deserialize(self, data_type: Type[dataclass_json]) -> dataclass_json
            Deserializes the data from the save file into the specified dataclass type.

        create(self) -> None
            Creates an empty save file.

        exists(self) -> bool
            Checks if the save file exists.

    Example:
        folder = Folder('/path/to/save/')
        save_file = SaveFile(folder, 'data')
        data = MyDataClass(some_field=42)
        save_file.serialize(data)
        loaded_data = save_file.deserialize(MyDataClass)
        if not save_file.exists():
            save_file.create()
    """
    EMPTY_FILE_STRING = "{}"

    def __init__(self, folder: Folder, data_type: Type[dataclass_json], file_name: str = "file"):
        """
        Initializes the SaveFile with a specified folder and file name.

        Args:
            folder (Folder): The folder where the save file should be located.
            data_type (Type[dataclass_json]): The type of data saved in this file
            file_name (str): The name of the save file (excluding the ".json" extension).
        """
        self._data_type: Type[dataclass_json] = data_type
        self._folder: Folder = folder
        self._file_path: str = os.path.join(self._folder.path, f"{file_name}.json")

    def serialize(self, data_content: dataclass_json) -> None:
        """
        Serializes the given data_content and writes it to the save file.

        Args:
            data_content (dataclass_json): The data to be serialized and saved into the file.
        """
        with open(self._file_path, 'w') as file:
            file.write(data_content.to_json())

    def deserialize(self) -> dataclass_json:
        """
        Deserializes the data from the save file into the specified dataclass type.

        Returns:
            dataclass_json: The deserialized data of the specified dataclass type.
        """
        with open(self._file_path, 'r') as file:
            data_string = file.read()
        return self._data_type.from_json(data_string)

    def create(self) -> None:
        """
        Creates an empty file.
        """
        with open(self._file_path, 'w') as file:
            data_string = SaveFile.EMPTY_FILE_STRING
            file.write(data_string)

    def exists(self) -> bool:
        """
        Checks if the save file exists.

        Returns:
            bool: True if the save file exists, False otherwise.
        """
        return os.path.exists(self._file_path)
