from __future__ import annotations
import os
from os import path
from typing import Callable

from App.ShowManager.Serializable import serializable


class SerializableDict(dict):
    """ This class describes a dictionary that manages serializable elements """

    def __init__(self, value_type: type, folder_path: str = ""):
        super().__init__()
        self._value_type = value_type
        self._folder: str = folder_path

    def create_element(self, name: str, on_folder_exists_cb: Callable[[serializable], None] | None = None,  *args, **kwargs) -> serializable:
        element_folder = path.normpath(path.join(self._folder, name))

        if not name:
            raise Exception("Element name must be provided")

        if name in self:
            element = self[name]
            if element.is_file_legal():
                if on_folder_exists_cb:
                    on_folder_exists_cb(element)
                    return element

        element = self._value_type(*args, **kwargs)
        element.name = name
        element.set_folder(element_folder)
        element.create_folder()
        element.serialize()
        self[name] = element
        return element

    def load_folder(self, folder_path: str | None = None) -> None:
        if folder_path:
            self._folder = folder_path

        self.clear()
        for folder_name in os.listdir(self._folder):
            path_to_folder = path.join(self._folder, folder_name)
            if path.isfile(path_to_folder):
                continue
            try:
                element = self._value_type.deserialize(path_to_folder)
            except:
                print(f"Error on deserializing {path_to_folder}")
                continue

            self[folder_name] = element

    def get_names(self) -> list[str]:
        """ Print the list of archived shows and return their name as a list """
        names = list(self.keys())
        return names

    def get_count(self) -> int:
        return len(self)

    def set_folder(self, folder_path: str):
        self._folder = folder_path

    def delete(self, key: str):
        self[key].delete_folder()
        del self[key]