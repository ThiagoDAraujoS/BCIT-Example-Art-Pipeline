from __future__ import annotations
import os
from os import path
from typing import Type

from .FolderManager import FolderManager


class SerializableDict(dict, FolderManager):
    """ This class describes a dictionary that manages serializable elements """

    def __init__(self, value_type: Type, folder_path: str = ""):
        dict.__init__(self)
        FolderManager.__init__(self)
        if not self._folder:
            self._folder = folder_path
        self._value_type: Type = value_type

    def create_element(self, name: str, *args, **kwargs) -> Type | None:
        element_folder = path.normpath(path.join(self._folder, name))

        if not name:
            raise Exception("Element name must be provided")

        if name in self:
            element = self[name]
            if element.is_file_legal():
                return None

        element = self._value_type(*args, **kwargs)
        element.set_folder(element_folder)
        element.create_folder()
        element.serialize()
        self[name] = element
        return element

    def load_from_folder(self, perform_recursive_load: bool = True) -> None:
        perform_recursive_load &= issubclass(self._value_type, SerializableDict)

        self.clear()
        for folder_name in os.listdir(self._folder):
            path_to_folder = path.join(self._folder, folder_name)

            if path.isfile(path_to_folder):
                continue

            try:
                element = self._value_type(path_to_folder)
                element.deserialize()
            except:
                print(f"Error on deserializing {path_to_folder}")
                continue

            if perform_recursive_load:
                element.load_from_folder()

            self[folder_name] = element

    def get_names(self) -> list[str]:
        return list(self.keys())

    def delete(self, key: str):
        self[key].delete_folder()
        del self[key]
