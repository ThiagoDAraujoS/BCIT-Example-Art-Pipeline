import os.path
from typing import Type
from dataclasses_json import dataclass_json

from .folder import Folder


class SaveFile:
    def __init__(self, folder, file_name):
        """
        Initialize a SaveFile instance.

        Args:
            folder (Folder): The folder where the SaveFile will be stored.
            file_name (str): The name of the SaveFile.
        """
        self.folder: Folder = folder
        self.file_path: str = os.path.join(self.folder.path, file_name)

    def serialize(self, data_content: dataclass_json):
        """
        Serialize the data content and save it to the SaveFile.

        Args:
            data_content (dataclass_json): The data content to be serialized.
        """
        with open(self.file_path, 'w') as file:
            file.write(data_content.to_json())

    def deserialize(self, data_type: Type[dataclass_json]) -> dataclass_json:
        """
        Deserialize the data from the SaveFile into the specified dataclass type.

        Args:
            data_type (Type[dataclass_json]): The type of the dataclass to deserialize to.

        Returns:
            dataclass_json: The deserialized data of the specified dataclass type.
        """
        with open(self.file_path, 'r') as file:
            data_string = file.read()
        return data_type.from_json(data_string)
