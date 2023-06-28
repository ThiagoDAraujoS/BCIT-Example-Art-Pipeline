import json
from os import path

FILE_NAME: str = "meta.data"
FILE_HEADER: str = "FILE CREATED BY: THIAGO dA. SILVA\nBCIT - Britsh Columbia Institute of Technology\nTechnical Arts Advanced Course\n"
FILE_DATA_BULLET: str = "DATA>>>\n"

def serializable(cls):
    """
    Decorator that adds serialization and deserialization methods to a class.

    The decorator adds the following methods to the decorated class:
    - serialize(): Serializes the object's variables and saves them into a file.
    - deserialize(folder_path: str): Loads the serialized data from a file and creates an object of the decorated class.
    """
    class SerializableClass(cls):
        def serialize(self) -> None:
            """
            Serializes the object's variables and saves them into a file.

            The object's variables are converted to JSON format and saved into a file.
            The file is created or overwritten with the serialized data, including the header text.
            """
            file_path = path.join(self.path, FILE_NAME)
            json_string = json.dumps(self.__dict__, indent=4)
            with open(file_path, "w") as file:
                file.write(f"{FILE_HEADER}{FILE_DATA_BULLET}{json_string}")

        @classmethod
        def deserialize(cls, folder_path: str) -> cls:
            """
            Loads the serialized data from a file and creates an object of the decorated class.

            The serialized data is loaded from the specified file, and the object of the decorated class is created.
            After the flag 'DATA>>>\n'the file must contain the serialized JSON data

            Args:
            - folder_path (str): The path to the folder containing the serialized file.

            Returns:
            - An object of the decorated class with the deserialized variables.

            Raises:
            - FileNotFoundError: If the specified file cannot be found.
            - json.JSONDecodeError: If the serialized JSON data is not valid.
            """
            file_path = path.join(folder_path, FILE_NAME)
            with open(file_path, "r") as file:
                file_string = file.read()
            json_string = file_string.split(FILE_DATA_BULLET)[-1]
            data = json.loads(json_string)
            obj = cls()
            obj.path = folder_path
            obj.__dict__.update(data)
            return obj

    return SerializableClass