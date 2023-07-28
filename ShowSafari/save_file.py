from .folder import Folder
import os.path
from dataclasses_json import dataclass_json


class SaveFile:
    def __init__(self, folder: Folder, data_reference: dataclass_json, file_name: str = "file"):
        self._data_reference = data_reference
        """ data_reference can only be an object or an dictionary """
        self._folder: Folder = folder
        self._file_path: str = os.path.join(self._folder.path, f"{file_name}.json")
        self.create()

    def save(self) -> None:
        json_string = self._data_reference.to_json()
        with open(self._file_path, 'w') as file:
            file.write(json_string)

    def load(self):
        with open(self._file_path, 'r') as file:
            data_string = file.read()
        self._data_reference.from_json(data_string)

    def create(self) -> bool:
        if self.exists():
            return False
        self.save()
        return True

    def exists(self) -> bool:
        return os.path.exists(self._file_path)
