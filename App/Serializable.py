import json
import os
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

                self._folder_path: str = path.normpath(folder_path) if folder_path else ""
                """ The folder where the serialized file lives in """

            def serialize(self) -> None:
                """ Serializes the object's variables and saves them into a file.

                The object's variables are converted to JSON format and saved into a file.
                The file is created or overwritten with the serialized data, including the header text. """

                data = {}
                for key, value in self.__dict__.items():
                    if key.startswith(NON_SERIALIZABLE_PREFIX):
                        continue

                    if isinstance(value, (date, time)):
                        value = value.isoformat()

                    if isinstance(value, set):
                        value = list(value)

                    data[key] = value

                json_string = json.dumps(data, indent=4)

                with open(self.get_file_path(), "w") as file:
                    file.write(f"{header_text}{FILE_DATA_BULLET}{json_string}")

            @classmethod
            def deserialize(cls, folder_path: str, *args, **kwargs) -> cls:
                """ Loads the serialized data from a file and creates an object of the decorated class

                The serialized data is loaded from the specified file, and the object of the decorated class is created.
                After the flag 'DATA>>>\n'the file must contain the serialized JSON data

                :param folder_path: The path to the folder containing the serialized file.
                :return: An object of the decorated class with the deserialized variables.

                :raise FileNotFoundError: If the specified file cannot be found.
                :raise json.JSONDecodeError: If the serialized JSON data is not valid. """

                def cast_special_types():
                    """ This method uses the cls to find the real types of the data stored in the file, then fixes the mistyped variables """
                    type_matrix = obj.__dict__
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

                obj = cls(folder_path=path.normpath(folder_path), *args, **kwargs)

                with open(obj.get_file_path(), "r") as file:
                    file_string = file.read().split(FILE_DATA_BULLET)[-1]

                data = json.loads(file_string)

                data = cast_special_types()

                obj.__dict__.update(data)
                return obj

            def get_file_path(self):
                """ Return the normalized metafile path """
                return path.normpath(path.join(self._folder_path, SerializableClass.META_FILE_NAME))

            def has_serialized_file(self):
                """ Predicate that returns if the serialized file exists """
                return path.exists(self.get_file_path())

            def make_directory(self):
                """ If folder_path directory doesn't exist this method can be used to create it """
                os.mkdir(self._folder_path)

            # TODO Implement a method that check if the serialized file is legal

        return SerializableClass
    return decorator
