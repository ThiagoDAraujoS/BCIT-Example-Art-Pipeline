import json
from os import path

FILE_NAME: str = "data.meta"
FILE_HEADER: str = "FILE CREATED BY: THIAGO dA. SILVA\nBCIT - Britsh Columbia Institute of Technology\nTechnical Arts Advanced Course\n"
FILE_DATA_BULLET: str = "DATA>>>\n"
NON_SERIALIZABLE_PREFIX: str = "_"

def serializable(cls):
    """
    Decorator that adds serialization and deserialization methods to a class.

    The decorator will not serialize private _members
    The decorator adds the following variables and methods to the decorated class:
    - self.path: the folder path for the serialized file
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

            file_path = path.join(self.path, FILE_NAME)
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

            def read_json_from_file():
                """ This method reads the contents of the file, then return a dictionary with its contents """
                file_path = path.join(folder_path, FILE_NAME)
                with open(file_path, "r") as file:
                    file_string = file.read()

                json_string = file_string.split(FILE_DATA_BULLET)[-1]

                return json.loads(json_string)

            def fix_mistypes(obj, data):
                """ This method uses the cls to find the real types of the data stored in the file, then fixes the mistyped variables """
                type_matrix = obj.__dict__
                for key, value in data.items():
                    if isinstance(type_matrix[value], time):
                        data[key] = time.fromisoformat(value)

                    elif isinstance(type_matrix[value], date):
                        data[key] = date.fromisoformat(value)

                    elif isinstance(type_matrix[value], set):
                        data[key] = set(value)

                    elif isinstance(type_matrix[value, tuple]):
                        data[key] = tuple(value)

                return data

            obj = cls()
            obj.path = folder_path

            data = read_json_from_file()
            data = fix_mistypes(obj, data)

            obj.__dict__.update(data)
            return obj

    return SerializableClass