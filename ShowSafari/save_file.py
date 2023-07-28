from ShowSafari import *
import os.path
from typing import Type
from dataclasses_json import dataclass_json


class SaveFile:
    EMPTY_FILE_STRING = "{}"

    def __init__(self, folder: Folder, data_reference: dataclass_json, file_name: str = "file"):
        self._data_reference = data_reference
        """ data_reference can only be an object or an dictionary """
        self._folder: Folder = folder
        self._file_path: str = os.path.join(self._folder.path, f"{file_name}.json")

    def serialize(self) -> None:
        with open(self._file_path, 'w') as file:
            file.write(self._data_reference.to_json())

    def deserialize(self):
        with open(self._file_path, 'r') as file:
            data_string = file.read()

        loaded_data = type(self._data_reference).from_json(data_string)

        if hasattr(self._data_reference, "__dict__"):
            self._data_reference.__dict__.update(loaded_data.__dict__)

        elif isinstance(self._data_reference, list):
            self._data_reference[:] = loaded_data

        else:
            self._data_reference.update(loaded_data)

    def create(self) -> bool:
        if self.exists():
            return False
        with open(self._file_path, 'w') as file:
            data_string = SaveFile.EMPTY_FILE_STRING
            file.write(data_string)
        return True

    def exists(self) -> bool:
        return os.path.exists(self._file_path)
