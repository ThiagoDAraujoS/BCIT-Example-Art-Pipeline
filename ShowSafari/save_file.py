import inspect

from .folder import Folder

import dataclasses
from dataclasses_json import dataclass_json
from typing import Type, Callable
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


def autosave(field_name: str):
    """
    Decorator to save a file associated with an instance after the decorated method is executed.

    This decorator is designed to work with a class instance that contains a `SaveFile` attribute.
    It saves the file using the provided reference attribute after the decorated method is executed,
    ensuring that the changes made during the method call are persisted.

    Parameters:
        field_name (str): The name of the attribute that holds the `SaveFile` instance in the class.

    Returns:
        Callable: A wrapper function that wraps the original method.

    Raises:
        ValueError: If the decorator is used on a static method or class method.
        AttributeError: If the field name does not exist in the class instance.

    Example usage:
        class MyClass:
            def __init__(self):
                self._save_file = SaveFile()

            @SaveFile.save_when_done("_save_file")
            def my_method(self, data):
                # Method implementation that modifies the data
                print("Method executed.")

        obj = MyClass()
        obj.my_method("some data")
        # After the method execution, the associated file is saved automatically.
    """

    def inner(func: Callable):
        def wrapper(self, *args, **kwargs):
            if inspect.isclass(self) or inspect.ismethod(func):
                raise ValueError("Decorator save_when_done cannot be used on static methods or class methods.")

            if not hasattr(self, field_name):
                raise AttributeError(f"Attribute '{field_name}' not found in the class instance.")

            result = func(self, *args, **kwargs)
            getattr(self, field_name).save()
            return result

        return wrapper

    return inner
