from __future__ import annotations
import os
import json

from .Show import Show
from .Serializable.SerializableDecorator import serializable
from .Serializable.SerializableDict import SerializableDict
from .Serializable.Serializable import Serializable, BuildExitCode

FILE_HEADER: str = """FILE CREATED BY: Thiago de Araujo Silva
BCIT - British Columbia Institute of Technology
Advanced Technical Arts Course
This file contains serialized show manager information."""


BOOKKEEPER_FILE_NAME = "projects.meta"


@serializable(FILE_HEADER)
class Manager(SerializableDict):
    """ The Manager class handles the management of shows and their associated files """

    def __init__(self, folder=""):
        super().__init__(Show, folder)
        self._bookkeeper_file = os.path.join(os.getcwd(), BOOKKEEPER_FILE_NAME)
        print(self._bookkeeper_file)

    def build(self, name, folder) -> BuildExitCode:
        # TODO SINCE I CHANGED SHOW THE FOLDER IS BUILD, IT MAKES NO SENSE I RETURN SO MANY RESPONSES
        project_path = os.path.join(folder, name)
        self.set_folder(project_path)
        return_code: BuildExitCode = Serializable.build(self)
        if return_code.SUCCESS:
            self._book_project(name, project_path)
        return return_code

    def _serialize_bookkeeper(self, data):
        with open(self._bookkeeper_file, "w") as file:
            file.write(json.dumps(data, indent=4))

    def _book_project(self, name, path):
        book = self.deserialize_bookkeeper()
        book[name] = path
        self._serialize_bookkeeper(book)

    def deserialize_bookkeeper(self) -> dict[str, str]:
        projects = {}
        if os.path.exists(self._bookkeeper_file):
            with open(self._bookkeeper_file, "r") as file:
                file_string = file.read()
                projects = json.loads(file_string)
            print(projects)
            return projects
        else:
            self._serialize_bookkeeper({})
        return projects
