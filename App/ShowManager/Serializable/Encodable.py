import json
from datetime import date, time

NON_SERIALIZABLE_PREFIX: str = "_"
""" Prefix used to indicate that a field should not be serialized when encoding an object into a JSON string. """


class Encodable:
    """ Provides methods to encode and decode data from and to a JSON string

    Methods:
        decode(json_string: str) -> None: Decode the JSON string into the object's fields.
        encode() -> str: Encode the object's fields into a JSON string.
    """

    def decode(self, json_string: str) -> None:
        """ Decode the JSON string into the object's fields. """
        type_matrix = self.__dict__
        data = {}
        for key, value in json.loads(json_string).items():
            if key not in type_matrix:
                continue

            if isinstance(type_matrix[key], time):
                data[key] = time.fromisoformat(value)

            elif isinstance(type_matrix[key], date):
                data[key] = date.fromisoformat(value)

            elif isinstance(type_matrix[key], set):
                data[key] = set(value)

            elif isinstance(type_matrix[key], tuple):
                data[key] = tuple(value)

            else:
                data[key] = value
        self.__dict__.update(data)

    def encode(self) -> str:
        """ Encode the object's fields into a JSON string. """
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
