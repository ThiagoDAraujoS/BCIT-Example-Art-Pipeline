import json
from os import path
from datetime import date, time


FILE_DATA_BULLET: str = "DATA>>>\n"
NON_SERIALIZABLE_PREFIX: str = "_"


def serializable(cls):
    def decorator(header_text: str = "", meta_file_name: str = "data"):
        """ Decorator that adds serialization and deserialization methods to a class

        The decorator will not serialize private _members
        The decorator adds the following variables and methods to the decorated class:
        - self.path: the folder path for the serialized file
        - serialize(): Serializes the object's variables and saves them into a file.
        - deserialize(folder_path: str): Loads the serialized data from a file and creates an object of the decorated class. """

        meta_file_name = f"{meta_file_name}.meta"
        class SerializableClass(cls):
            def __init__(self, folder_path, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._path = folder_path

            def serialize(self) -> None:
                """
                Serializes the object's variables and saves them into a file.

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

                file_path = path.join(self._path, meta_file_name)
                with open(file_path, "w") as file:
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

                def read_json_from_file():
                    """ This method reads the contents of the file, then return a dictionary with its contents """
                    file_path = path.join(folder_path, meta_file_name)
                    with open(file_path, "r") as file:
                        file_string = file.read()

                    json_string = file_string.split(FILE_DATA_BULLET)[-1]

                    return json.loads(json_string)

                def fix_mistypes():
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

                obj = cls(*args, **kwargs)
                obj._path = folder_path

                data = read_json_from_file()
                data = fix_mistypes()

                obj.__dict__.update(data)
                return obj

        return SerializableClass
    return decorator
