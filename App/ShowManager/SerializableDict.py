from __future__ import annotations
import os
from os import path
from typing import Callable

from App.ShowManager.Serializable import serializable


class SerializableDict(dict):
    """ This class describes a dictionary that manages serializable elements """

    def __init__(self, value_type: type, folder_path: str = ""):
        """ Initializes a SerializableDict instance

        :param value_type: The type of the values to be stored in the dictionary.
        :param folder_path: The folder path where the serialized elements will be stored. Defaults to an empty string.
        """
        super().__init__()
        self._value_type = value_type
        self._folder: str = folder_path

    def create_element(self, name: str, on_folder_exists_cb: Callable[[serializable], None] | None = None,  *args, **kwargs) -> serializable:
        """ Creates a new serializable element with the provided name

        :param name: The name of the element.
        :param on_folder_exists_cb:  Callback function to be called if the element's folder already exists. Defaults to None.
        :param args & kwargs: Additional arguments to be passed to the constructor of the value type.
        :return: The created serializable element.
        """
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

    def load_folder(self, folder_path: str | None = None, perform_recursive_load: bool = True) -> None:
        """ Loads serialized elements from a folder

        :param folder_path: The folder path from which to load the serialized elements.
            If None, uses the previously set folder path.
            Defaults to None.
        :param perform_recursive_load: Flag indicating whether to perform recursive loading of nested SerializableDict elements.
            Defaults to True.
        """
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

            if perform_recursive_load and issubclass(self._value_type, SerializableDict):
                element.load_folder(os.path.join(self._folder, folder_name), True)

            self[folder_name] = element

    def get_names(self) -> list[str]:
        """ Returns a list of the names of the serialized elements

        :return: A list of the names of the serialized elements.
        """
        names = list(self.keys())
        return names

    def get_count(self) -> int:
        """ Returns the number of serialized elements in the dictionary

        :return: The number of serialized elements in the dictionary.
        """
        return len(self)

    def set_folder(self, folder_path: str) -> None:
        """ Sets the folder path where the serialized elements will be stored.

        :param folder_path: The folder path where the serialized elements will be stored.
        """
        self._folder = folder_path

    def delete(self, key: str):
        """ Deletes a serialized element and its files with the specified key

        :param key: The key of the serialized element to be deleted.
        """
        self[key].delete_folder()
        del self[key]
