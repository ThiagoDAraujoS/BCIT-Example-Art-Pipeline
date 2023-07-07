import json
import os
import shutil
from os import path
from datetime import date, time


FILE_DATA_BULLET: str = "\nDATA>>>\n"
NON_SERIALIZABLE_PREFIX: str = "_"


def serializable(header_text: str = "", meta_file_name: str = "data"):
    """ Decorator that adds serialization and deserialization methods to a class

    The decorator will not serialize private _members
    The decorator adds the following variables and methods to the decorated class:
    - self.folder_path: the folder path for the serialized file
    - serialize(): Serializes the object's variables and saves them into a file.
    - deserialize(folder_path: str): Loads the serialized data from a file and creates an object of the decorated class.
    - get_file_path(self): Return the path to the serialized file
    - has_serialized_file(self): Return if the serialized path exists """

    def decorator(cls):
        class SerializableClass(cls):
            META_FILE_NAME: str = f"{meta_file_name}.meta"
            """ Constant full serialized file name """

            def __init__(self, folder_path: str = "", *args, **kwargs):
                super().__init__(*args, **kwargs)

                self._folder: str = path.normpath(folder_path) if folder_path else ""
                """ The folder where the serialized file lives in """

            def print(self) -> str:
                """ Same as Encode, but it prints the contained data before returning """
                data = self.encode()
                print(data)
                return data

            def unpack(self, file_string: str) -> str:
                """ Rips the header out of the file_string and return the remainder data as a dictionary """
                return file_string.split(FILE_DATA_BULLET)[-1]

            def decode(self, json_string: str) -> dict:
                """ This method decode file text into a cls field dictionary

                :returns: dictionary of field names mapped to their values recorded in the text """
                data = json.loads(json_string)
                type_matrix = self.__dict__
                result_data = {}
                for key, value in data.items():
                    if key not in type_matrix:
                        continue

                    if isinstance(type_matrix[key], time):
                        result_data[key] = time.fromisoformat(value)

                    elif isinstance(type_matrix[key], date):
                        result_data[key] = date.fromisoformat(value)

                    elif isinstance(type_matrix[key], set):
                        result_data[key] = set(value)

                    elif isinstance(type_matrix[key], tuple):
                        result_data[key] = tuple(value)

                    else:
                        result_data[key] = value
                return result_data

            def encode(self) -> str:
                """ This method encodes objects fields into a file text

                :returns: a json string containing all the obj's data + header text """
                data = {}
                for key, value in self.__dict__.items():
                    if key.startswith(NON_SERIALIZABLE_PREFIX):
                        continue

                    if isinstance(value, (date, time)):
                        value = value.isoformat()

                    if isinstance(value, set):
                        value = list(value)

                    data[key] = value
                return json.dumps(data, indent=4)

            def serialize(self) -> None:
                """ Serializes the object's variables and saves them into a file.

                The object's variables are converted to JSON format and saved into a file.
                The file is created or overwritten with the serialized data, including the header text. """

                file_text = f"{header_text}{FILE_DATA_BULLET}{self.encode()}"

                with open(self.get_file(), "w") as file:
                    file.write(file_text)

            @classmethod
            def deserialize(cls, folder_path: str, *args, **kwargs) -> cls:
                """ Loads the serialized data from a file and creates an object of the decorated class

                The serialized data is loaded from the specified file, and the object of the decorated class is created.
                After the flag 'DATA>>>\n'the file must contain the serialized JSON data

                :param folder_path: The path to the folder containing the serialized file.
                :return: An object of the decorated class with the deserialized variables.

                :raise FileNotFoundError: If the specified file cannot be found.
                :raise json.JSONDecodeError: If the serialized JSON data is not valid. """
                obj = cls(folder_path=path.normpath(folder_path), *args, **kwargs)

                with open(obj.get_file(), "r") as file:
                    file_string = file.read()

                json_string = obj.unpack(file_string)
                data = obj.decode(json_string)
                obj.__dict__.update(data)
                return obj

            def get_folder(self):
                """ return folder path """
                return self._folder

            def set_folder(self, folder_path):
                """ Setter for the folder path variable """
                self._folder = folder_path

            def create_folder(self):
                """ If folder_path directory doesn't exist this method can be used to create it """
                os.mkdir(self._folder)

            def delete_folder(self):
                """ Delete the serialized folder and its contents """
                if self.folder_exists():
                    shutil.rmtree(self._folder)

            def folder_exists(self):
                """ Return if the _folder_path exists """
                return path.exists(self._folder)

            def get_file(self):
                """ Return the normalized metafile path """
                return path.normpath(path.join(self._folder, SerializableClass.META_FILE_NAME))

            def file_exists(self):
                """ Predicate that returns if the serialized file exists """
                return path.exists(self.get_file())

            def is_file_legal(self):
                """ Predicate that verify if the serialized file is legal """
                try:
                    with open(self.get_file(), "r") as file:
                        file_string = file.read()
                    file_string = file_string.split(FILE_DATA_BULLET)[-1]
                    data = json.loads(file_string)
                    type_matrix = self.__dict__
                    for key, _ in data.items():
                        if key not in type_matrix:
                            raise Exception(f"Data missmatch between {cls} to file text")
                except:
                    return False
                return True

        return SerializableClass
    return decorator
