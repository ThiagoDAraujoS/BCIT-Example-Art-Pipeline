from __future__ import annotations
import os
import warnings
from os import path
from typing import Type
from enum import Enum
from .FolderManager import FolderManager
from .Serializable import Serializable


class CreateElementExitCode(Enum):
    SUCCESS, NO_NAME_PROVIDED, ELEMENT_EXISTS, CREATION_ERROR = 0, 1, 2, 3


class LoadFromFolderExitCode(Enum):
    SUCCESS, NO_FOLDER_FOUND = 0, 1


class SerializableDict(dict, FolderManager):
    """ This class describes a dictionary that manages serializable elements """

    def __init__(self, value_type: Type, folder_path: str = ""):
        dict.__init__(self)
        FolderManager.__init__(self)
        if not self._folder:
            self._folder = path.normpath(folder_path)
        self._value_type: Type = value_type

    def create_element(self, name: str, *args, **kwargs) -> CreateElementExitCode:
        """ Create an element in the dictionary, then build a folder and metafile for said element. """
        element_folder = path.normpath(path.join(self._folder, name))

        if not name:
            return CreateElementExitCode.NO_NAME_PROVIDED

        if name in self:
            return CreateElementExitCode.ELEMENT_EXISTS

        try: element = self._value_type(*args, **kwargs)
        except: return CreateElementExitCode.CREATION_ERROR

        element.set_folder(element_folder)
        element.create_folder()
        element.serialize()
        self[name] = element
        return CreateElementExitCode.SUCCESS

    def load_from_folder(self, perform_recursive_load: bool = True) -> LoadFromFolderExitCode:
        """ Load a folder's contents and deserialize all metafiles corresponding to this dictionary's _value_type"""
        perform_recursive_load &= issubclass(self._value_type, SerializableDict)

        if not self.folder_exists():
            return LoadFromFolderExitCode.NO_FOLDER_FOUND

        self.clear()
        for folder_name in os.listdir(self._folder):
            path_to_folder = path.join(self._folder, folder_name)

            if path.isfile(path_to_folder):
                continue

            try:
                element = self._value_type(path_to_folder)
                if element.file_exists():
                    element.deserialize()
            except:
                warnings.warn(f"Error on deserializing {path_to_folder}")
                continue

            self[folder_name] = element

            if perform_recursive_load:
                element.load_from_folder()

        return LoadFromFolderExitCode.SUCCESS

    def get_names(self) -> list[str]:
        """ Get a list of elements names stored in this dictionary """
        return list(self.keys())

    def delete(self, key: str):
        """ Delete an element from the dictionary and its folder """
        self[key].delete_folder()
        del self[key]
