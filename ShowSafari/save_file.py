from .folder import Folder

import dataclasses
from dataclasses_json import dataclass_json
from typing import Type
import os.path


class SaveFile:
    def __init__(self, folder: Folder, data_reference: dataclass_json, file_name: str = "file"):
        """ Initializes a SaveFile object.

            If a physical file does not exist a new one will be generated.

            Else, the existing file will be loaded onto data_reference.

        Parameters:
            folder (Folder): The folder where the data file will be saved.
            data_reference (dataclass_json): Reference to the dataclass object to be saved.
            file_name (str, optional): The name of the data file (without extension). Defaults to "file".
        """
        self._data_reference: dataclass_json = data_reference
        """ The dataclass object to be saved """

        self._reference_type: Type[dataclass_json] = type(self._data_reference)
        """ The type of the dataclass object being saved """

        self._folder: Folder = folder
        """ The folder where the data file will be saved """

        self._file_path: str = os.path.join(self._folder.path, f"{file_name}.json")

        """ The path of the JSON file to be saved/loaded """
        if not self.exists():
            self.save()
        else:
            self.load()

    def save(self) -> None:
        """
        Serializes and saves the dataclass object to a JSON file with indentation.
        """
        json_string = self._data_reference.to_json(indent=2)
        with open(self._file_path, 'w') as file:
            file.write(json_string)

    def load(self):
        """
        Loads the data from the existing JSON file into the dataclass object.
        """
        with open(self._file_path, 'r') as file:
            data_string = file.read()

        loaded_instance = self._reference_type.from_json(data_string)

        for field in dataclasses.fields(self._reference_type):
            loaded_value = getattr(loaded_instance, field.name)
            setattr(self._data_reference, field.name, loaded_value)

    def exists(self) -> bool:
        """
        Checks if the JSON file exists in the specified folder.

        Returns:
            bool: True if the file exists, False otherwise.
        """
        return os.path.exists(self._file_path)
